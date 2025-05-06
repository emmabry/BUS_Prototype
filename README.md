# UniSupport

System description

## Step-by-step instructions

**Appointment Viewing and Booking**
1.	Click on the ‘Appointment’ tab on the navigation bar at the top. This will display a table with all upcoming appointments for the user, including the advisor’s name, data, time and location.
    - Clicking on the ‘View Details’ button will display all other information about the appointment that was not displayed previously. This includes the advisor’s organisation and the reason for the appointment.
    - Click the ‘Back to Appointments’ button to return to the upcoming appointments web page.
      
2.	Click on the ‘Book Appointment’ button to redirect to a form in order to book an appointment. All fields of the form are required except the reason behind the appointment. 
      - _Test Case One – Positive_
          - Select one of the advisors from the drop-down list
          - Select a weekday (Monday – Friday)
          - Select a time between 9 am and 5 pm, which doesn’t overlap with any events (confirmed through the ‘Calendar’ page)
          - Add a reason, although this is not required
          - Select a ‘location’ from the drop-down list
          - Click ‘Book Appointment’. The 'Upcoming Appointments' page will be rendered with a message that the appointment was booked successfully. The booked appointment will now also be visible in the table.
            
      - _Test Case Two – Negative_
          - Select one of the advisors from the drop-down list
          - Select a weekend (Saturday or Sunday)
          - Select any time
          - Add a reason, although this is not required
          - Select a ‘location’ from the drop-down list
          - Click ‘Book Appointment’. A message will appear, stating that the advisor is unavailable on that day.



## Languages & Frameworks Used

- Python
- Flask
- JavaScript
- HTML/CSS
- Bootstrap

## Implemented Functionalities

Dashboard & Quiz: 

The dashboard shows personalised feature recommendations based on the user answers to an onboarding quiz, which are stored in a database table. If the user has not taken the onboarding quiz, the dashboard will show a card prompting them to take the quiz. Otherwise, it will show feature recommendations and article recommendations based on quiz answers.

Calendar: 

Users can add events to their calendar, where they can input a title, a description, location and start and end times and dates. Based on the end date and time, the user will receive a notification reminder 1 hour before the event.

Appointment Booking: 

On the Appointments page the user can book a new appointment with an advisor and set a date, time and appointment location. This feature is linked to the calendar tool, where booked appointments will automatically show on the calendar.

#### Features
- Calendar
- Dashboard
- Quiz
- Appointment booking

#### Design Pattern
- Publish-Subscribe
- Singleton pattern for database

#### Relationships
- Inheritance between User class and Student, Staff, ExternalProfessional classes
- Inheritance between Event class and Appointment class
- Aggregation between Calendar class and Event class

### Test cases

## Contribution

| Student Name & ID             | Contribution (%) | Key Contributions / Tasks Completed                                                                                                                             | Comments (if any) | Signature    |
|-------------------------------|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|--------------|
| Emma Bryan - 2647065          | 25%              | [Task description]                                                                                                                                              | [Comments]        | [Signature]  |
| Martyna Ofiara - 2204418      | 25%              | [Task description]                                                                                                                                              | [Comments]        | [Signature]  |
| Amy Baker - 2720905           | 25%              | [Task description]                                                                                                                                              | [Comments]        | [Signature]  |
| Rosemary Burningham - 2001897 | 25%              | Onboarding quiz implementation and recommendation feature on dashboard, README document system description, implemented functionalities summary and commit logs |                   | R Burningham |
| Humna Arooj Farooq - 2331550  | 0%               |                                                                                                                                                                 |                   |              |
