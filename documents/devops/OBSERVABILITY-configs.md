# Observability configuration sketches

Companion to [OBSERVABILITY.md](OBSERVABILITY.md), section 10. These are starting points and have not been run. Pin image versions instead of `latest`. Service names match the figures: `dispatch`, `issue`, `auth`.


These are starting points and have not been run. Pin image versions instead of `latest`. The Loki and Alloy configuration is not included here and should be written against the Alloy docs for the version you pick.

### `observability/prometheus.yml`

```yaml
global:
  scrape_interval: 30s

scrape_configs:
  - job_name: node
    static_configs: [ { targets: ["node-exporter:9100"] } ]

  - job_name: cadvisor
    static_configs: [ { targets: ["cadvisor:8080"] } ]

  - job_name: services
    static_configs: [ { targets: ["dispatch:8080", "issue:8080", "auth:8080"] } ]

  - job_name: rabbitmq          # only if RabbitMQ is used
    static_configs: [ { targets: ["rabbitmq:15692"] } ]

  - job_name: blackbox
    metrics_path: /probe
    params: { module: [http_2xx] }
    static_configs: [ { targets: ["https://<your-domain>/readyz"] } ]
    relabel_configs:
      - { source_labels: [__address__], target_label: __param_target }
      - { source_labels: [__param_target], target_label: instance }
      - { target_label: __address__, replacement: "blackbox:9115" }
```

### `docker-compose.observability.yml`

```yaml
services:
  prometheus:
    image: prom/prometheus:<pinned-version>
    command:
      - --config.file=/etc/prometheus/prometheus.yml
      - --storage.tsdb.retention.time=15d
      - --storage.tsdb.retention.size=2GB
    volumes:
      - ./observability/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    ports: ["127.0.0.1:9090:9090"]      # localhost only
    restart: unless-stopped

  grafana:
    image: grafana/grafana:<pinned-version>
    environment:
      GF_SECURITY_ADMIN_PASSWORD__FILE: /run/secrets/grafana_admin_password
    secrets: [grafana_admin_password]
    volumes:
      - grafana-data:/var/lib/grafana
    ports: ["127.0.0.1:3000:3000"]      # localhost only
    restart: unless-stopped

  node-exporter:
    image: prom/node-exporter:<pinned-version>
    command: ["--path.rootfs=/host"]
    pid: host
    volumes: ["/:/host:ro,rslave"]
    restart: unless-stopped

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:<pinned-version>
    privileged: true
    devices: ["/dev/kmsg"]
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    restart: unless-stopped

  rabbitmq:                      # only if RabbitMQ is used; no public ports
    image: rabbitmq:<pinned-version>   # enable the rabbitmq_prometheus plugin
    restart: unless-stopped

  blackbox:
    image: prom/blackbox-exporter:<pinned-version>
    restart: unless-stopped

volumes:
  prometheus-data:
  grafana-data:

secrets:
  grafana_admin_password:
    file: ./secrets/grafana_admin_password   # not committed
```

### Log rotation for every service

Without this, container logs can fill the disk.

```yaml
logging:
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"
```

---

