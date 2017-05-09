#Laboratory Work 1
##Problem Description

You suddenly hear the awesome news that your grand-grand-uncle's cousin, that left to Nigeria a long time ago, has left you with quite a piece of land in the wonderful Telenești area near Budăi (total area is about 1,2 sq. km). You, a huge fan of linear programming, have built this map in order to see things more clearly.

At some point you have decided to grow some crops on this field. Upon consulting the specialists, you arrive to the following options:

- Each 0.1 sq. km of land (not forest) needs 200 lei/month to be taken care of
- Each 0.1 sq. km of the forest costs 100 lei/month for its care
- Keep in mind that you have limited territory for forests! Measure it! Note: Consider that you
pay these two at the end of the year out of the profits.
- At least 0.5 sq km of the forest needs to be kept
- You can invite hunters into the forest. The estimated profit there is around 20K lei/sq.km/year
- The potato seeds cost you 100 lei/sq. km
- From each 0.1 sq km of the field you can collect 1 ton of potatoes
- Potatoes can be farmed twice a year.
- A potato tractor costs 500lei/sq. km (It collects your potatoes)
- A ton of potatoes can be sold on the market with 2K lei
- You can also make wine (of course!). Grape seeds cost you 800 lei/sq. km. For simplicity, let’s consider that it’s a yearly investment. (You kill all the grape plants each year)
- Each 0.1 sq. km of land can give you 2 tons of grapes / year
- The people that collect the grapes need to be paid (there’s no wine yet). They ask for 5000lei/sq. km
- You can make 400 litres of wine with 1 ton of grapes
- The wine is sold at 6 lei/litre

Unfortunately, although your kind uncle gave you the land, he didn’t give you the money, so you put together three months worth of student’s scholarships (a total of 1500 lei) and set out to create the greatest farming empire Budăi has ever seen.

Considering that you’re a fan of linear programming, how do you go about organizing this area? What will you farm and how much of the area will you farm?

Using your result, develop a simulation that will show your income over time. Use per-year estimations to develop your method. How will this method change if you consider that you won’t have to put the grapes in again each year? How will this change considering that you will pay the grape collectors 2 times less, but give them 100 liters of wine instead?

##Solution

In order to solve the problem it was devided into 3 modules:
- Simplex module - that was responsible for the calculation. More about the simplex that i used can be found [here](http://www.zweigmedia.com/RealWorld/tutorialsf4/framesSimplex2.html).
- Business module - that was responsible for finding the values needed to feed to simplex class. Here all 3 cases were implmented. Also here we obtain the values needed to diplay in our simulation
- Simulation module - whos purpose was to display the data obtained in the previous 2 modules. In order to display them dinamically for each year was used the ```Tkinter module```. More about it [here](https://docs.python.org/2/library/tkinter.html).

When the application is launched you should select what case you want to solve. And then press ```space key``` in order to find the solution for this year. And so on.

The surface of colors displayed are proportionally corelated to the solution for each year ```green, yellow, purple``` respectivelly for ```forest, potatoes, grape area```.
