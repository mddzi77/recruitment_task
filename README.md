# Recruitment Task
REPL program that allows user to make reservation for a tennis court

Screen that will welcome you:
```
Welcome to tennis court reservation
->
```

You can write your commands or values after ```-> ```

## Create a reservation
To make reservation enter command ```Make a reservation```.
You will be asked your name, surname and date, time and length of reservation
```
What's your name?
-> Aaa Bbb
When would you like to book? (DD.MM.YYYY HH:MM)
-> 29.03.2023 15:30
How long would you like to book court?
1) 30 Minutes
2) 60 Minutes
3) 90 Minutes
-> 2
You successfulyy booked a court for 29.03.2023 15:30:00
```
At any point you can go back to main menu by entering ```back``` or ```b```.<br>
Limit for reservations per week is 3.

## Cancel a reservation
To cancel your reservation enter command ```Cancel a reservation```.
You have to enter the same name and date which you used for making reservation.
```
What's your name?
-> Aaa Bbb
What was the time of the reservation? (DD.MM.YYYY HH:MM)
-> 29.03.2023 15:30
You cancelled your reservation
```

## Print schedule of reservations
You can view schedule of reservations from chosen period of time by using a ```Print schedule``` command.
You will have to enter start and end point of your chosen time range.
Output example:
```
27.03.2023:
  Aaa Bbb 15:30 - 16:30
Yesterday:
  No reservations
Today:
  Ccc Ddd 15:00 - 16:30
  Aaa Bbb 16:30 - 17:00
```
After printing out schedule you will be brought back to main menu.

## Save schedule to a file
You can save to file the schedule of reservations from chosen period of time,to do it enter ```Save schedule```.<br>
There are two file formats possible: csv and json, which you will have to chose after giving time range.
The last thing is to enter a file name.
Example:
```
Please enter start and end for period for which You want to get schedule (DD.MM.YYYY-DD.MM.YYYY)
-> 26.03.2023-30.03.2023
Choose file format (csv or json)
-> json
Enter a file name
-> schedule
File saved succesfully!
```

## Additional notes
- ```h``` or ```help``` entered in main menu will give you list of possible commands
- exit program at any point using ```q``` or ```quit``` (will not take effect while entering file name)
- you can go back to main menu and cancel entering data with ```b``` or ```back``` (like with ```quit``` will not take effect while entering file name)
- commands are not case-sensitive

### Author
:pen: Maksymilian Dziemiańczuk  :email: md.dziem@gmail.com
