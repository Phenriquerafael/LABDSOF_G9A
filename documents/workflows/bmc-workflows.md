# BMC — Proposed workflows (with diagrams)


## Ground rules

- The AI classifies and chooses a contractor and a date, but only proposes. The administrator accepts or refuses.
- The resident only reports, follows progress, confirms "this affects me too" and requests a cancellation. Residents do not approve bookings.
- Issue status: **reported → triaged → proposal sent → booked → completed → closed**. Detours: cancelled (goes back to "to be scheduled") and reopened.

## 1. Condominium registration

![Workflow 1: condominium registration](images/01-condominium-registration.png)

1. The user creates an account and registers the organisation and the first building in the same step.
2. They become the administrator of that organisation.
3. The system creates the condominium space.
4. For each fraction (apartment unit), the administrator generates an **e-invite** (single use, valid for 7 days) and emails it to the resident.

## 2. Resident joins by e-invite

![Workflow 2: resident joins by e-invite](images/02-resident-joins-by-invite.png)

1. The resident opens the e-invite link and creates an account (or signs in, if they already have one).
2. They are linked automatically to the building and the fraction on the invite, with no approval step.
3. If the invite has expired or was already used, they ask the administrator for a new one.

## 3. Report an issue

![Workflow 3: report an issue](images/03-report-an-issue.png)

1. The resident enters the building and the zone and describes the problem in text.
2. The system saves the report and immediately returns a **confirmation with a reference number**.
3. The report goes on to the AI analysis (workflow 4), without the resident having to wait.

If the analysis fails, the report is still saved. The resident follows the status through the reference number.

## 4. AI analysis and proposal (automatic)

![Workflow 4a: AI classification](images/04a-ai-classification.png)

![Workflow 4b: contractor matching and proposal](images/04b-contractor-matching-and-proposal.png)

1. Receives the report (text, building and zone).
2. Suggests the category and the **maintenance priority** (low, medium or high), with a plain-language reason.
3. If the AI fails, the report goes to the administrator as "classify by hand".
4. Filters the compatible contractors: specialty matches the category, coverage area includes the building, and at least one free slot **this week**. Availability comes from the schedule the contractor set at registration (workflow 9), minus the bookings already accepted.
5. Ranks the remaining ones by availability, **price**, straight-line **distance** and, as a bonus, already having another booking in the same building that day. Picks the best option and builds the **proposal** with the reason, for example "free Thursday at 10:00, 4 km, €60 per visit".
6. Saves everything as an **unverified suggestion** and notifies the administrator. If nobody is free this week, the issue is marked "awaiting manual coordination".

High-priority issues are notified first.

## 5. Administrator approval

![Workflow 5: admin approval](images/05-admin-approval.png)

1. The administrator receives the notification with the full proposal: classification, contractor, day, time, price, distance and reason.
2. **Accepts:** the classification is confirmed and the request goes to the contractor as a **temporary** booking.
3. **Refuses**, with a reason: the AI proposes the next option, or the administrator picks by hand and can correct the classification. Any change is recorded with author and reason.

Nothing goes to the contractor without the administrator's acceptance.

## 6. Contractor response

![Workflow 6: contractor response](images/06-contractor-response.png)

1. The contractor receives the request: problem, location, day, time and price. They never see the resident's original text.
2. **Accepts:** the booking goes from temporary to **final** and enters the calendar. The administrator and the resident are notified.
3. **Declines:** the AI proposes the next option to the administrator (workflow 4).
4. If the contractor does not respond within the set deadline, the administrator is alerted.

"Confirmed" is only shown to the resident when the booking is really final.

## 7. Cancel a booking

![Workflow 7a: cancel by admin or contractor](images/07a-cancel-by-admin-or-contractor.png)

![Workflow 7b: resident cancellation request](images/07b-resident-cancellation-request.png)

There is no "change": to move a date, cancel and create a new booking through workflows 4 and 5.

1. The administrator or the contractor cancels the booking **up to 24h before**, with a mandatory reason.
2. The resident can **request** the cancellation, and the administrator decides.
3. The booking is removed from the calendar, but the history is kept.
4. All parties are notified and the issue goes back to "to be scheduled".
5. Within 24h, only the administrator can cancel, and it is recorded as an exception.

## 8. Execution and closure

![Workflow 8a: execution](images/08a-execution.png)

![Workflow 8b: closure and reopening](images/08b-closure-and-reopening.png)

1. On the booked date, the contractor does the work and marks it "in progress", and then "completed". The issue becomes "awaiting validation".
2. Optional: the contractor or the administrator records the cost. Residents do not see it.
3. The administrator validates and **closes** the issue. The resident is notified.
4. If it is not resolved, the administrator sends it back to the contractor with a reason and the issue goes back to "to be scheduled".
5. A closed issue can be **reopened**, with a reason. Everything stays in the history.

## 9. Contractor registration

![Workflow 9: contractor registration](images/09-contractor-registration.png)

1. The contractor creates an account and enters the company, the specialties, the coverage area and the base address (used to calculate distance).
2. Sets the price: **per visit** or **per hour**, their choice.
3. Sets the **usual weekly schedule** (for example, Monday to Friday, mornings and afternoons) and can block specific days (holidays, another job). Each accepted booking takes up a slot.
4. The team validates the registration by hand.
5. Once validated, the contractor enters the catalogue and can receive requests.

In the workflow 4 ranking, the price appears as entered (€/visit or €/h), with no conversion.

## 10. "This affects me too"

![Workflow 10: this affects me too](images/10-this-affects-me-too.png)

1. The administrator publishes a **shared summary** of the problem for the building, without identifying who reported it or any private data.
2. The other residents see it and tap "this affects me too" instead of reporting again.
3. The administrator sees how many residents are affected, which helps decide the priority. They can link reports of the same problem, keeping the originals.
4. Residents follow the status of the issue in the same summary, without seeing costs or the contractor's terms.

## Notification table

| Event | Who is notified |
|---|---|
| Invite sent | Resident |
| Report received | Resident (confirmation with reference number) |
| Proposal ready | Administrator |
| Request sent | Contractor |
| Contractor accepts or declines | Administrator |
| Booking final | Administrator and resident |
| Booking cancelled | Administrator, contractor and resident |
| Summary published | Residents of the building |
| Work completed | Administrator |
| Issue closed or reopened | Resident |

One channel only in the MVP (for example, email). The resident can turn notifications off.

## Decisions made

- [x] The AI analysis has its own workflow and is automatic: it classifies, filters contractors and proposes.
- [x] The AI chooses the contractor and the date; the administrator is notified and accepts or refuses.
- [x] Emergencies (gas, fire) stay outside the app. Urgency is only maintenance priority: low, medium or high.
- [x] Contractor availability is set at registration (workflow 9) and read by workflow 4.
- [x] Residents join by e-invite only (per fraction, single use, 7 days). No request-to-join in the app.
- [x] Bookings can only be created and deleted. Changing a booking no longer exists.
- [x] The resident can only request a cancellation; the administrator decides.
- [x] The 24h cancellation window is fixed for now.
- [x] Scheduling covers the current week only, using availability, existing bookings, price and straight-line distance.
- [x] The contractor creates their own account, validated by the team, with a price per visit or per hour.
- [x] "This affects me too" is a separate workflow (10). Notifications live in a reference table.
- [x] Resident management (revoking invites, moving out, several administrators) is left for after the MVP.
