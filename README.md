# StarHacks
StarHacks Submission
First, we will create a data class called Person with instance attributes that correspond with the following categories: Age Groups in Increments of 10, the Severity of Generalized Anxiety, the Mental health Compared to Before Physical Distancing, the Concern about impact of COVID-19 - Canadian population’s health, the Concern about impact of COVID-19 - Maintaining social ties, the Perceived Mental Health and COVID-19 impacts ability meet financial obligations or essential needs. 


In the first function, the data file is opened there's a comprehension that iterates through each row of the data file and calls the process_row function with each row.


The process_row function will take in a row, select the elements at the specific indices that correspond to the attributes, convert them into int or float data types, and assign each of them to the corresponding instance attribute for the data class. This function will return an instance of the Person data class.


After the data is processed, we will make a function that takes in a string representing one of the attributes and an age group to find the average of that attribute for each age group. This function will also filter out any numbers representing an unanswered questions. (ie. for a question with the answer range 1-5, 9 represents no answer)


For our overall graph, we will make a new function that uses a nested loop to loop through each of the age groups, and each of the category averages for each age group. We will then convert the score into a percentage and multiply it by its assigned weight value, then sum it to create our composite factor which takes into account all of the categories. The function will return a list of 6 floats representing the overall score for each age group.


Then, we will define 12 empty lists: 6 lists for each age group, each of which will later consist of data class instances, and another 6 lists (1 per attribute) that will contain the average of the attribute for each age group.


Next, a function will be made to go through each Person and sort it into the correct age group using if statements.


The next function runs the example and takes in a string of the data file. Inside the function, there is a list of strings of the attribute names and a list of the age groups (which themselves are lists of all the Person objects in a particular age range). For each attribute average list, we will insert a tuple of the lowest number possibly selected for a question, the highest number possibly selected, and the number code given in the case that the participant did not answer. A for loop will append each attribute average list to a new list. We will call our load file function on the data file and loop through all the people and sort them into age groups. Next, a nested for loop will go through each age group within each attribute and calculates the averages and adds it to a list. Another nested loop is used to a dictionary that maps the group number to a list of the averages for each attribute for that group. And then it calls another function to plot the data.


The final function will take in a dictionary and a list of strings of attributes in order to plot the data. We obtain the first element of each of the averages list (this tuple contains the range for the attribute). Then we create a figure and add traces to make 8 graphs, one for each of the 6 attributes, one for the composite factor, and one showing all of the lines together. We also made a menu of buttons that when clicked, display each of the graphs.
