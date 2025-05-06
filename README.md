# UniSupport

System description

## Step-by-step instructions

**Running the application locally**
1. In the terminal, call 'flask shell'.
2. Inside the flask shell, call 'reset_db()' in order to populate the database.
3. Run flask to start the program.
4. To log in, use any of the test users in debug_utils.py

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

3. Once an appointment is booked, this will also automatically pull through to the calendar.

**Calendar**
1. After navigating to the calendar page (/calendar), click the blue 'Add Event' button on the left to create an event, and fill in the form with the event details.
2. Once an event is created, you will be redirected back to the calendar. You can click on the eye symbol to the right of the event to open up the event details.
3. To edit an event, you can click the pen symbol to the right of the event.
4. To delete an event, you can click the trashcan symbol to the right of the event.
5. On the top right hand side of the event page, you can navigate through the calendar with the 'previous', 'today', and 'next' buttons.

**Quiz and Dashboard**
1. Upon logging in for the first time, the user will be prompted to take an onboarding quiz. This will gather data on what the user struggles the most with.
2. After completing the onboarding quiz, the user will be redirected to the dashboard, where they will have personalised feature/article recommendations based on the onboarding quiz results.


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

#### Design Patterns
- Publish-Subscribe pattern for calendar notifications
- Singleton pattern for database

#### Relationships
- Inheritance between User class and Student, Staff, ExternalProfessional classes
- Inheritance between Event class and Appointment class
- Aggregation between Calendar class and Event class

## Contribution

| Student Name & ID             | Contribution (%) | Key Contributions / Tasks Completed                                                                                                                             | Comments (if any) | Signature    |
|-------------------------------|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|--------------|
| Emma Bryan - 2647065          | 25%              | Implemented calendar functionality, set up database inheritance & aggregation, set up project structure, walkthrough video.                                     |                   | E Bryan      |
| Martyna Ofiara - 2204418      | 25%              | Implemented appointment booking functionality, set up appointment classes in database                                                                           | [Comments]        | [Signature]  |
| Amy Baker - 2720905           | 25%              | Implemented Publish-Subscribe pattern for calendar notifications, implemented positive and negative test cases                                                  | [Comments]        | [Signature]  |
| Rosemary Burningham - 2001897 | 25%              | Onboarding quiz implementation and recommendation feature on dashboard, README document system description, implemented functionalities summary and commit logs |                   | R Burningham |
| Humna Arooj Farooq - 2331550  | 0%               |                                                                                                                                                                 |                   |              |
