# CEC 2019
The repository for CEC 2019!

## Problem Statement
As automation becomes increasingly present in our lives, blue-collar jobs with simple forms of labour are now being replaced with robots. This allows the company to complete the same amount of work as previously at a fraction of the cost. Assembly line work is the first being automated, but it is slowly expanding into other sectors such as services. Companies who would like to save money and be able to grow more rapidly are already turning to these solutions. By 2020, McDonalds will have most of its 14,000 locations and hundreds of thousands of staffed cashiers replaced by order kiosk. Most warehouse moving jobs, especially at bigger companies like Amazon, have been replaced with robots. With automation increasing in other industries, such as transportation and home appliances, it’s inevitable that the only part of the services industry of the future that will be human are the customers.

Res-TRON-t Solutions (RS) is an automation company that specializes in creating robots that serve purposes in restaurant settings. They’ve become very successful due to their production line cleaning service product for large food courts and drive-thru automation product line, however they would like to grow their market share in the semi-formal eatery industry. Establishments that serve food but also are used for other purposes, such as board game cafes or Starbucks, usually leave their staff to clean up their mess, which usually involves transferring garbage, recyclables and organics to their disposal bins. These establishments usually have the closing staff clean up the place after hours, as well as have them check tables and clean periodically throughout the day. Additionally, waste will often not be properly sorted which causes lots of recyclables and organics to be improperly sent to landfills, and garbage to be sent to recycling or organics facilities.

However, RS would like to reduce the need of staff even further and increase the sorting effectiveness of trash. Due to their licensing of other companies’ technology, engineers at the company have been able to program a device using a modified autonomous vacuum cleaner that can interact with surfaces off the floor, such as tables and bar stools. It can collect pieces of trash, and place them in the appropriate disposal bins.

RS would like you to develop a software solution to help control the robot and enable it to clean the trash efficiently. Garbage, recyclables, and organics will be scattered in a dining room and it is your job to navigate the robot to clean all of them. This software will communicate with the robot via REST API, and will be given access to various commands that will help it locate, retrieve, and place tableware. Efficiency is key, and software that can help optimize this problem will help it be used in real-time situations. You must present your product to the company board (judges) by focusing on its simplicity, ingenuity, and ability to achieve its desired outcome. The code for your application must be submitted using email and optionally a USB device, along with instructions on how to run it in a README file. This software can be written in any language and will communicate using rate-limited API calls to a simulation server.

## Objectives
Your goal with this task is to design a robot that can cleanup the entire eatery space in the fastest possible amount of time. After completing the code, submit it, along with instructions on how to run it, using email and optionally a USB device. Please read the Programming rulebook for deadlines and all submission instructions. Read and follow all the rules!

## Materials
An access token to the simulation server via API will be provided. A design room with at least one table, four chairs, a whiteboard or blackboard, paper and pencils/pens for writing, as well as access to a computer with internet connectivity, will be provided during the 8-hour design phase. A presentation room with a digital projector, a computer containing the team’s presentation file, a whiteboard or blackboard, and simultaneous translation equipment if required will be provided during the presentation phase.

## Environment Setup
Make sure you have `pipenv` installed then run the following command.
```
# if you are using pipenv
pipenv install --skip-lock [--dev]
```

## Running
Activate your virtual environment the run the following command.
```
python main.py
```

## Testing
Make sure you have the dev dependencies installed and your virtual environment activated then run the following command.
```
pytest
```
