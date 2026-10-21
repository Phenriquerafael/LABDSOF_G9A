# CI/CD Strategy

This document describes our branching model, pipelines, golden images, security testing and release process.

---

## 1. Principles

1. **Build once, promote the same artifact.** What is tested is exactly what ships. Prod never triggers a rebuild.
2. **Dev is automatic, prod is deliberate.** Merges to `dev` deploy by themselves. Production is only released by a protected version tag.
3. **Everything is built on golden images.** Hardened, scanned, signed base images that we own and version.
4. **Security is part of the pipeline**, not a separate phase (SAST, SCA, secrets, container scan, DAST).
5. **Everything is traceable.** Every running version maps to a tag, a commit, an SBOM and a signature.

---

## 2. Branching model

| Branch | Purpose | Who can merge into it | Protection | Deploys to |
|---|---|---|---|---|
| `main` | Production-ready code | **Tech leads and DevOps only** | Protected, PR + approvals + passing checks, no direct pushes | Prod (only via tag) |
| `dev` | Integration of finished work | **Anyone** with write access | Protected, PR + passing checks (+ 1 approval) | Dev environment (automatic) |
| `feature/*`, `fix/*`, any other | Short-lived work branches (QA) | n/a (anyone can push) | None | Nothing |

See [section 11](#11-access-control-and-roles) for how this is enforced.

![Branching model: feature branches merge into dev, dev merges into main, main is tagged](images/branching-gitgraph.png)

Flow of code: `feature/*` → PR → `dev` → PR → `main` → tag `vX.Y.Z` → production.

---

## 3. Pipeline overview

| Trigger | Build | Tests + SAST + SCA + secrets | Push image to GHCR | Container scan + SBOM + sign | Deploy | DAST |
|---|---|---|---|---|---|---|
| Any other branch / PR | yes | yes | no | scan only | no | no |
| Push to `dev` | yes | yes | yes (`dev-<sha>`) | yes | **auto to dev** | yes |
| Push to `main` | yes | yes | yes (`sha-<sha>`) | yes | no | optional (staging) |
| Tag `v*` on `main` | no (promote) | verify only | retag (`vX.Y.Z`) | verify signature | **prod** | no |

![Pipeline overview for feature branches, dev, main and release tags](images/pipeline-overview.png)

---

## 4. Golden images

Golden images are our own hardened base images (runtime, language, tooling). Application Dockerfiles **only** build `FROM` a golden image, never directly from Docker Hub.

### What makes an image "golden"

- Built from a minimal upstream (distroless, Alpine, or a slim Debian/Ubuntu)
- Non-root user by default, no shell or package manager in runtime variants
- Only the required packages and dependencies
- Scanned with **zero unwaived critical/high CVEs**
- SBOM generated and attached
- **Signed** with cosign
- Published to GHCR and **pinned by digest** by consumers

### Lifecycle

![Golden image lifecycle: build, scan, SBOM, sign, push, digest bump](images/golden-image-lifecycle.png)

### Rules

- **Rebuild on a schedule** (e.g. weekly) and whenever the upstream image or a critical CVE changes.
- **Pin by digest** in app Dockerfiles: `FROM ghcr.io/<org>/golden-node@sha256:<digest>`.
- Let **Renovate/Dependabot** open PRs to bump the digest, so updates go through the normal pipeline.
- Keep golden images in their **own repository** with their own pipeline and release cadence.

Example app Dockerfile:

```dockerfile
# Build stage
FROM ghcr.io/<org>/golden-node-build@sha256:<digest> AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM ghcr.io/<org>/golden-node-runtime@sha256:<digest>
WORKDIR /app
COPY --from=build /app/dist ./dist
USER nonroot
CMD ["dist/main.js"]
```

---

## 5. Security testing

| Check | Tool examples | What it finds | When it runs |
|---|---|---|---|
| **Secrets scan** | gitleaks, GitHub secret scanning | Leaked credentials | Every push/PR |
| **SAST** | CodeQL, Semgrep | Vulnerabilities in our source code | Every push/PR |
| **SCA** | Dependabot, `npm audit`, OSV-Scanner, Trivy fs | Vulnerable dependencies and licence issues | Every push/PR |
| **IaC / Dockerfile scan** | Trivy config, Checkov, hadolint | Misconfigurations | Every push/PR |
| **Container scan** | Trivy, Grype | CVEs in the final image | Every image build |
| **SBOM** | Syft, Trivy | Inventory of components | Every image build |
| **Image signing** | cosign (keyless via GitHub OIDC) | Integrity / provenance | Every pushed image |
| **DAST** | OWASP ZAP (baseline / full scan) | Runtime issues (XSS, injection, headers, auth) | After deploy to **dev** |

### About DAST

DAST needs a **running application**, so it cannot run on feature branches (nothing is deployed there). It runs against the **dev environment** right after the automatic deployment:

![DAST sequence against the dev environment](images/dast-sequence.png)

Suggested policy:
- **Block** the PR/merge on SAST, secrets, and critical/high container or dependency findings.
- **Block promotion** to prod if the latest DAST on dev has high findings.
- Waivers must have an owner and an expiry date.

---

## 6. Registry and image tagging (GHCR)

All images live in GitHub Container Registry: `ghcr.io/<org>/<app>`.

| Event | Tags pushed | Notes |
|---|---|---|
| Push to `dev` | `dev-<sha>`, `dev` (moving) | Used by the dev environment |
| Push to `main` | `sha-<sha>` | The release candidate |
| Tag `v1.4.0` | `1.4.0`, `1.4`, `1` | **Retag** of the `sha-<sha>` image, never a rebuild |

Avoid deploying `latest`. Deploy by **version tag or digest**. Old `dev-*` images are pruned automatically, see [section 10](#10-ghcr-cleanup-retention).

Every image is:
- **Signed** with cosign (keyless, GitHub OIDC)
- Published with an **SBOM** and build **provenance** attestation
- Deployed only after its **signature is verified**

---

## 7. Releasing to production by tag

Production is triggered only by pushing a `v*` tag. The pipeline **does not rebuild**: it finds the image already built and tested for that commit on `main`, verifies it, and retags it.

![Release sequence: tag, verify, promote and deploy to production](images/release-sequence.png)

### How to release

```bash
git checkout main && git pull
git tag -a v1.4.0 -m "Release 1.4.0"
git push origin v1.4.0
```

### Safeguards

- **Tag ruleset** (Settings → Rules → Rulesets): only named tech leads and DevOps can create `v*` tags.
- Pipeline **fails if the tagged commit is not on `main`**.
- Pipeline **fails if no signed image exists** for that commit (meaning it never passed CI).
- Optional: GitHub **Environment `production`** with required reviewers (manual approval).

### Rollback

Redeploy a previous version tag: `ghcr.io/<org>/<app>:1.3.2`. No rebuild needed, since the image still exists in GHCR. Keep a retention policy that never deletes released version tags.

---

## 8. GitHub Actions skeleton

Suggested workflow files:

```
.github/workflows/
├── ci.yml          # any branch / PR: build, test, SAST, SCA, scan
├── dev.yml         # push to dev: build, push, sign, deploy dev, DAST
├── main.yml        # push to main: build, push sha-<sha>, sign
├── release.yml     # tag v*: verify, retag, deploy prod, GitHub Release
└── ghcr-cleanup.yml # weekly: prune old dev-* images (dry run first)
```

### `ci.yml` (any branch except dev and main)

```yaml
name: CI
on:
  pull_request:
  push:
    branches-ignore: [dev, main]

permissions:
  contents: read
  security-events: write

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Secrets scan
        uses: gitleaks/gitleaks-action@v2
      - name: Build and test
        run: |
          make build
          make test
      - name: SAST (CodeQL)
        uses: github/codeql-action/init@v3
      - uses: github/codeql-action/analyze@v3
      - name: Build image (not pushed)
        run: docker build -t app:ci .
      - name: Container scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: app:ci
          severity: CRITICAL,HIGH
          exit-code: "1"
```

### `release.yml` (tag)

```yaml
name: Release
on:
  push:
    tags: ["v*"]

permissions:
  contents: write
  packages: write
  id-token: write

jobs:
  promote:
    runs-on: ubuntu-latest
    environment: production        # optional manual approval
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }

      - name: Ensure tag is on main
        run: |
          git merge-base --is-ancestor "$GITHUB_SHA" origin/main \
            || { echo "Tag is not on main"; exit 1; }

      - uses: sigstore/cosign-installer@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Verify signature of the tested image
        run: |
          cosign verify ghcr.io/${{ github.repository }}:sha-${{ github.sha }} \
            --certificate-identity-regexp "https://github.com/${{ github.repository }}/.*" \
            --certificate-oidc-issuer https://token.actions.githubusercontent.com

      - name: Promote (retag, no rebuild)
        run: |
          VERSION=${GITHUB_REF_NAME#v}
          docker buildx imagetools create \
            -t ghcr.io/${{ github.repository }}:${VERSION} \
            ghcr.io/${{ github.repository }}:sha-${{ github.sha }}

      - name: Deploy to prod
        run: ./scripts/deploy.sh prod ${GITHUB_REF_NAME#v}

      - name: GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
```

> These are starting points. Adjust build commands, deploy scripts and tool versions to the real stack.

---

## 9. Secrets and variables

GitHub's equivalent of GitLab CI/CD variables are **secrets** (encrypted, masked in logs, write-only) and **variables** (plain configuration, visible). Both are set under Settings → Secrets and variables → Actions, and used as `${{ secrets.NAME }}` and `${{ vars.NAME }}`.

### 9.1 Rules

- **Never commit secrets, and never bake them into images.** `ARG` and `ENV` values end up in image layers.
- **Narrowest scope wins:** environment secret over repository secret.
- **Production secrets live only in the `production` environment**, which is limited to `v*` tags (and approval, if enabled). See section 11.
- **Separate credentials for dev and prod.** A leaked dev credential must never work in prod.
- **Prefer OIDC** (short-lived cloud credentials, nothing stored) over long-lived keys wherever the provider supports it.
- **Pass a secret only to the step that needs it,** through `env:`, and never print it.
- **Every long-lived credential has an owner, an expiry date and a rotation reminder.**

### 9.2 What lives where

| Item | Type | Scope | Used by |
|---|---|---|---|
| `GITHUB_TOKEN` | Automatic, per run | The workflow run | GHCR push, retag, GitHub Release (permissions set per job) |
| `SONAR_TOKEN` (if SonarQube is used) | Secret | Repository | CI workflow |
| Dev deploy credentials | Secret | Environment `dev` | `dev.yml` deploy job |
| Prod deploy credentials | Secret | Environment `production` | `release.yml` only |
| `GHCR_CLEANUP_PAT` | Secret (classic PAT) | Repository | `ghcr-cleanup.yml` only, see section 10 |
| App URLs, registry name, feature toggles | Variable | Repository or environment | Any workflow |
| Tokens that Dependabot PRs need (for example the Sonar token) | Dependabot secret | Repository | Dependabot-triggered runs |

### 9.3 Usage

```yaml
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment: production          # unlocks the production secrets
    steps:
      - name: Deploy
        run: ./scripts/deploy.sh "${GITHUB_REF_NAME#v}"
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
          APP_URL: ${{ vars.APP_URL }}
```

### 9.4 GitLab to GitHub

| GitLab | GitHub |
|---|---|
| CI/CD variable (masked) | Secret (always masked) |
| Plain variable | Variable (`vars.*`) |
| Environment scope | Environment secrets |
| Protected variable (protected branches and tags only) | Environment with deployment branches and tags limited to `v*` |
| Group-level variable | Organization secret (needs an organization) |
| File-type variable | No equivalent: write the value to a file inside a step |

### 9.5 Gotchas

- **Fork PRs do not receive secrets.** That protects you on a public repo, but it means checks that need a secret (for example a Sonar scan) must be skipped or run only for same-repo PRs.
- **Dependabot has its own secret store.** Dependabot PRs cannot read normal Actions secrets.
- **Anyone who can edit a workflow can read the secrets it uses,** for example by pushing a workflow that sends the value somewhere. That is why prod secrets sit in a restricted environment and why section 11 limits who can touch `main` and release tags.
- **Masking only hides the exact value.** A transformed value (base64, a substring, a URL-encoded copy) is not masked, so avoid printing derived forms.
- **A single secret is limited to about 48 KB.** Larger files need another approach.

---

## 10. GHCR cleanup (retention)

Without cleanup, every merge to `dev` and `main` adds images that nobody will ever deploy again. The goal is to keep the registry small without deleting anything you need for rollback, audit or signature verification.

### 10.1 Retention policy

| What | Policy | Why |
|---|---|---|
| Release tags (`1.4.0`, `1.4`, `1`) and the image they point to | **Keep forever** | Rollback and audit |
| `sha-<sha>` images built on `main` | **Keep for now** | A released image is the same image as its `sha-<sha>` tag, so they share one package version |
| `dev-<sha>` images built on `dev` | **Delete after 30 days, always keep the 10 newest** | They are never promoted to prod, so pruning them is safe |
| Cosign signatures and attestations (tags such as `sha256-<digest>.sig`) | **Never touch** | Needed to verify released images |
| Untagged versions | **Never delete by hand** | Often the per-platform children or attestations of a tagged image |

Because only `dev-*` images are pruned, a released image can never be hit by the cleanup.

### 10.2 Do you need a PAT?

- **To publish and promote images: no.** `GITHUB_TOKEN` with `packages: write` is enough.
- **To delete image versions: it depends.** GitHub documents that a workflow's `GITHUB_TOKEN` can delete versions of packages that belong to the workflow's repository, as long as the repository has the **Admin** role on the package (Package settings → Manage Actions access). GitHub labels this capability a public preview, so it may change.
- **The catch:** the retention action recommended below cannot use its wildcard and tag filters with `GITHUB_TOKEN`. To prune only `dev-*` images you need a **personal access token (classic)** or a GitHub App token.
- **PAT type:** GitHub Packages only supports **classic** PATs, not fine-grained ones. Scopes: `read:packages` and `delete:packages`.
- **Treat it as sensitive.** A classic PAT is tied to a person, is long-lived, and can delete **any** package that person can access. Store it as the repository secret `GHCR_CLEANUP_PAT`, use it only in the cleanup workflow, give it an expiry date (for example 90 days) and set a reminder to rotate it. After a move to an organization, a GitHub App token with `packages: write` is the cleaner option.

### 10.3 Workflow (`ghcr-cleanup.yml`)

```yaml
name: GHCR cleanup
on:
  schedule:
    - cron: "0 3 * * 0"             # weekly, Sunday 03:00 UTC
  workflow_dispatch:
    inputs:
      dry_run:
        description: "Only log what would be deleted"
        type: boolean
        default: true

permissions:
  contents: read

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: snok/container-retention-policy@<commit-sha>   # v3.x, pin by SHA and confirm the latest release
        with:
          account: user                          # personal account; use the org name after a transfer
          token: ${{ secrets.GHCR_CLEANUP_PAT }}
          image-names: "<app>"                   # the package name, without the ghcr.io/<owner>/ prefix
          image-tags: "dev-*"                    # only prune dev builds
          tag-selection: tagged
          cut-off: 30d
          keep-n-most-recent: 10
          dry-run: ${{ github.event_name == 'workflow_dispatch' && inputs.dry_run }}
```

This is a starting point that has not been run against your registry. Check the input names against the README of the version you pin.

### 10.4 Rollout and traps

1. **Dry run first.** Trigger the workflow manually with `dry_run` on, read the log, and confirm only `dev-*` versions are listed. Only then let the weekly schedule run.
2. **Multi-platform and attested images:** an image can consist of several untagged child manifests. Deleting those breaks the tagged image that points to them. The action protects the children of the tagged versions it keeps, but keeping the filter on `dev-*` is the safest setup.
3. **Signatures:** the action's documentation does not cover cosign signatures. Keep the tag filter on `dev-*` so release signatures are never candidates. Signatures of deleted dev images will remain as small orphaned versions, which is harmless.
4. **Public packages:** GitHub does not allow deleting a version of a public package if any version of it has more than 5,000 downloads.
5. **Mistakes can be undone for 30 days:** a deleted package or version can be restored within 30 days, as long as the name has not been reused.

---

## 11. Access control and roles

> This section assumes a **public repository owned by a personal GitHub account** on the Free plan. Everything below is available at no cost in that setup. If the project outgrows it, see [11.5](#115-when-to-move-to-an-organization).

### 11.1 Who can do what

| Action | Who | Enforced by |
|---|---|---|
| Push to `feature/*`, `fix/*` | Any collaborator | No restriction |
| Merge QA branch into `dev` | **Any collaborator** | Ruleset on `dev`: PR + checks + 1 approval |
| Merge `dev` into `main` | **Named tech leads and DevOps** | Two rulesets on `main` (quality rules + merge gate) |
| Create a `v*` tag (release to prod) | **Named tech leads and DevOps** | Tag ruleset |
| Approve the prod deployment | **Named DevOps** | Environment `production` required reviewers |
| Change pipelines (`.github/`, Dockerfiles, infra) | DevOps reviewers | CODEOWNERS |
| Change repo settings, rulesets, secrets | **Repo owner only** | Owner role |

![Who can merge and release at each step](images/access-control-flow.png)

### 11.2 Roles on a personal repository

A personal repository has only two permission levels, so "tech lead" and "DevOps" do not exist as GitHub roles. They become **lists of usernames** in rulesets, environments and CODEOWNERS.

| Level | What it can do |
|---|---|
| **Owner** (exactly one) | Everything: settings, rulesets, environments, secrets, collaborators |
| **Collaborator** | Read and write: push to unprotected branches, open and merge PRs (subject to the rulesets) |
| Anyone else | Read the public repo, fork it, open PRs from their fork. No write access. |

There are no teams, and no Triage, Maintain or Admin roles. Mapping for this project:

| Project role | In GitHub |
|---|---|
| Developers | Collaborators |
| Tech leads | Collaborators, listed in the `main-gate` ruleset, the tag ruleset and CODEOWNERS |
| DevOps | The repo owner, plus any collaborators listed as `production` reviewers |
| External contributors | Fork + PR only |

Since there is only one Owner, whoever owns the account is effectively the admin. Other DevOps people can approve and merge, but cannot change settings.

### 11.3 How to set it up

**1. Add collaborators:** Settings → Collaborators → Add people (these get Write access).

**2. Ruleset for `dev`** (anyone can merge). Settings → Rules → Rulesets → New branch ruleset:
- Name `dev-quality`, enforcement **Active**, target branch `dev`, **no bypass list**
- Require a pull request before merging (1 approval)
- Require status checks to pass (build, test, SAST, container scan)
- Block force pushes, restrict deletions

**3. Two rulesets for `main`** (only tech leads and DevOps can merge)

A bypass actor skips **every rule in the ruleset it is listed in**. To keep the merge restriction without letting gatekeepers skip the quality rules, split them into two rulesets. Rules from different rulesets stack, and a bypass only applies to the ruleset it is listed in.

| Ruleset | Target | Rules | Bypass list |
|---|---|---|---|
| `main-quality` | `main` | Require PR with 1-2 approvals (and Code Owner review), require status checks, block force pushes, restrict deletions | **None** |
| `main-gate` | `main` | **Restrict updates** (nobody can update `main`, including by merging a PR, unless on the bypass list) | Named tech leads and DevOps users |

Result: only the listed people can merge into `main`, and they still need an approved PR with passing checks. Test it once with a dummy PR from a non-listed account.

The author of a PR cannot approve it, so keep at least two people able to approve.

**4. CODEOWNERS** (`.github/CODEOWNERS`) protects the pipeline itself:

```
# Pipelines, images and infrastructure need DevOps approval
/.github/        @<owner-username>
/Dockerfile      @<owner-username>
/infra/          @<owner-username>
```

Keep this limited to sensitive paths. A `*` entry would force an approval from those owners on every PR into `dev` as well.

**5. Tag ruleset** (Settings → Rules → Rulesets → New tag ruleset)
- Target: tags matching `v*`
- Rules: restrict creations, restrict updates, restrict deletions
- Bypass list: named tech leads and DevOps users (the only ones who can create release tags)

**6. Environments** (Settings → Environments)

| Environment | Settings |
|---|---|
| `dev` | No reviewers. Deployment branches: `dev` only. |
| `production` | Required reviewers: named DevOps users (up to 6). Prevent self-review. Deployment branches and tags: `v*` only. **Do not** allow administrators to bypass. Prod secrets live here, never at repo level. |

If there is only one DevOps person, "prevent self-review" would block them from approving their own release. Turn it off in that case, or add a second reviewer.

**7. Hardening for a public repo** (Settings → Actions → General)
- Require approval to run workflows from first-time contributors
- Default `GITHUB_TOKEN` permissions: read-only, elevate per job
- Pin third-party actions by commit SHA
- Never expose secrets to fork PRs, and avoid `pull_request_target` unless you fully understand it
- Check the GHCR package visibility after the first push, since a public repo's package may be publicly pullable

### 11.4 Limits of a personal account

- **One owner, no co-admins.** If that person is unavailable, nobody else can change settings.
- **Everything is a list of usernames.** Adding or removing a tech lead means editing `main-gate`, the tag ruleset, the environment reviewers and CODEOWNERS.
- **Bypass is powerful.** Keep the bypass lists as short as possible.

### 11.5 When to move to an organization

Creating a **free organization** and transferring the repository (Settings → Danger Zone → Transfer) removes those limits. Rulesets are available for public repositories on the Free plan for organizations too. You get:

- **Teams** (`developers`, `tech-leads`, `devops`), so rulesets, CODEOWNERS and environments point to a team instead of individual usernames
- **Repository roles:** Read, Triage, Write, Maintain and Admin (custom roles are Enterprise only)
- **Several admins**, and organization roles (Owner, Member, Billing manager, Security manager, and others)
- **Branch restrictions** ("restrict who can push") on organization-owned repos

After a transfer, the GHCR image path changes from `ghcr.io/<user>/<app>` to `ghcr.io/<org>/<app>`, so update the workflows and any deployment manifests.

---

## 12. Repository settings checklist

- [ ] Rulesets on `dev` and `main` (PR required, status checks required, no force push), see section 11.3
- [ ] Tag ruleset for `v*`, limited to named tech leads and DevOps
- [ ] GitHub Environments: `dev` (no approval), `production` (required reviewers, optional)
- [ ] Secret scanning and push protection enabled
- [ ] Dependabot / Renovate enabled (dependencies, Docker digests, Actions)
- [ ] GHCR package visibility and access configured, retention policy excludes version tags (section 10)
- [ ] Golden image repo with scheduled rebuild workflow
- [ ] Workflow permissions default to read-only, elevated per job
- [ ] Cosign verification enforced before any deploy
- [ ] Collaborators added with Write access; the repo owner acts as DevOps / final authority
- [ ] `main-gate` ruleset lists only the tech leads and DevOps; `dev` stays open to collaborators
- [ ] CODEOWNERS covers `.github/`, Dockerfiles and infra
- [ ] Environment `production` has required reviewers and is limited to `v*` tags
- [ ] Bypass lists and environment reviewers kept to the minimum number of people
- [ ] Secrets: prod credentials only in the `production` environment, dev and prod credentials separate (section 9)
- [ ] `GHCR_CLEANUP_PAT` created (classic, `read:packages` + `delete:packages`), has an expiry date and a rotation reminder
- [ ] GHCR cleanup workflow run once as a dry run and the log reviewed before enabling the schedule

---

## 13. Quick reference

| I want to... | Do this |
|---|---|
| Work on a change | Branch from `dev` as `feature/<name>`, open PR to `dev` |
| See my change on dev | Merge PR to `dev` (anyone), pipeline deploys automatically |
| Prepare a release | Open PR `dev` → `main` (merged by a tech lead or DevOps) |
| Ship to production | Tag `vX.Y.Z` on `main` and push the tag (tech lead or DevOps only) |
| Roll back | Redeploy the previous version tag |
| Update base images | Merge the Renovate/Dependabot digest bump PR |
| Clean old images | Run `ghcr-cleanup.yml` manually with dry run on, review, then let the weekly schedule run |
