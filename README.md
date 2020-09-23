# Robot-In-ROS

This project is about the development of a robotic agent that travels in a world, finds objects and answers questions that are asked by the user. This world is a floor in a hotel.
The robot is inside a simulator called Stage, and Stage works in ROS, which is the Robot Operating System. 


  
Possible categories are the following: bed, book, chair, computer, door, per- son, table. Note that other categories might be present. The categories names’ are always a single word.
Individual objects receive names that always include the category first, such as: person_joe, book_alice_in_wonderland, table_table1, computer_windows2.
There are five room types, all of them can have tables and chairs:
• if the room contains one individual bed, it is a single room;
• if the room contains two individual beds, it is a double room;
• if there are beds and an internal door (that connects to another room) then it is a suite;
• if the room contains only one table and several chairs it is a meeting room
• rooms that are none of the above are called generic rooms
 
We say that a room is occupied if there is at least one person in it.


The Robot answer the following questions:
  1. How many rooms are not occupied?
  2. How many suites did you find until now?
  3. Is it more probable to find people in the corridors or inside the rooms?
  4. If you want to find a computer, to which type of room do you go to?
  5. What is the number of the closest single room?
  6. How can you go from the current room to the elevator?
  7. How many books do you estimate to find in the next 2 minutes?
  8. What is the probability of finding a table in a room without books but that has at least one chair?
