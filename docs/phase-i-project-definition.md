# Project Definition Phase I


## Project Objectives (Phase I)

1. To gain experience with the design and development of a relatively larger software project
2. To gain practical experience in OOP design and development, interacting with a data base
    and GUI implementation.
3. To gain the experience of real-world data analysis.
4. To use engineering tools (python packages) to design and analysing engineering problems


## Phase I (GUI and DataBase)

### The purpose of the first phase of the project is to get familiar with the python

### Graphic User Interface (GUI) and use a database for keeping required data.

### In the first phase, you will write a GUI application that manages traffic information

### from Calgary city. The required data is available on Calgary city website

### (https://data.calgary.ca/browse?sortBy=newest).


## GUI

### The python GUI that you are developing must have the following functionalities:

- It should be able to read and write the traffic information from/to database and

### keep it in the right data structure

- It should be able to display the traffic records information on the computer

### screen.

- The user should be able to select type of information and corresponding year

### for doing analysis.

- You should be able to load the calgary city map and you should be able to

### show the maximum traffic volume or accident based on the year on the map.


## System Design

The GUI must have two frames: the left frame is control frame which includes buttons and gets

input from user, the right frame is for drawing the table of information and the statistics that we

need to visualize.

```
Left
Frame
```
```
Right Frame
```

## System Design (Left Frame Functionality)

(^) 1. It must include two rows: accident and Traffic Volume (Type Combobox)

2. It must keep the information of the years that we have accident and traffic data
    (Type Combobox (2016, 2017, 2018))
3. According to type and year, it must read the corresponding data and print a table of
    rows in right_frame (Type Button)
4. It must sort data based on the maximum traffic volume or maximum accident.
    (Type Button)
5. It must draw a chart in right frame which draws the maximum number of accidents
    and traffic volume according to the year (Type Button)
6. Map should write the map of Calgary in map.html file and marks the section that
    has the maximum accident or traffic volume. (Type Button)
7. It should show the status of system any error in reading database or drawing chart
    should be printed in this message bar. (Type Label)

```
Read
```
```
Status:
```
```
Type
```
```
Year
```
```
Sort
```
```
Analysis
```
```
Status
Messages
```
#### 1

#### 2

#### 3

#### 4

#### 5

```
Map
```
#### 6

#### 7


## Example Setting for left frame and right frame data

## display (Read Button)

```
Read
```
```
Status:
```
```
Traffic Vol
```
```
2016
```
```
Sort
```
```
Analysis
```
```
Successfully
read from DB
```
```
Map
```

## Example Setting for left frame and right frame data

## display (Sort Button)

```
Read
```
```
Status:
```
```
Traffic Vol
```
```
2016
```
```
Sort
```
```
Analysis
```
```
Successfully
sorted
```
```
This should be sorted based on volume if the table is traffic
volume and the number of incidents if it is the number of
accidents information
```
```
Map
```

## Example Setting for left frame and right frame data

## display (Analysis Button)

```
Read
```
```
Status:
```
```
Traffic Vol
```
```
2016
```
```
Sort
```
```
Analysis
```
```
Successfully
analyzed
```
```
Max Volume or number of accidents
(Y-axis)
```
```
Year (X-axis)
Map
```

## Example Setting for left frame and right frame data

## display (Analysis Button)

```
Read
```
```
Status:
```
```
Traffic Vol
```
```
2016
```
```
Sort
```
```
Analysis
```
```
Successfully
analyzed
```
#### 2016 2017 2018

#### 1000

#### 500

#### 100

```
Map
```

## Example Setting for left frame and right frame data

## display (Analysis Button)

```
Read
```
```
Status:
```
```
Traffic Vol
```
```
2016
```
```
Sort
```
```
Analysis
```
```
Successfully
Written Map
```
```
Map
```
```
Must write an html file called map.html which includes the map of calgary
city and the location that have the maximum accident or traffic
```

## Packages

### Here is the suggestion of some packages you can use for the project:

- Database: Mongodb

- GUI: tkinter

- Drawing map: folium

### You are free to use any other types of packages and modules for database, gui, and drawing map.


## Marking

- Read and write to the database: 5 Marks

- Sort the data and find the max value: 5 Marks

- Analyzing data and drawing chart: 5 Marks

- Map drawing and writing the map.html: 5 Marks

- Project Demo: 5 Marks

- Total Mark: 25 Marks

- Due date: 23 July-


