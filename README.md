readme.txt - Lab 4


-- IMPORTANT NOTE --
I do NOT own the original Solitaire API and do not take credit for it. You can find the original one here: https://github.com/chuan-yu/Solitaire-Game-API 

I took this API and converted it to Pydantic Base Models and SQLAlchmey/SQLite models. You can compare the two as the original is included in the repo.


By no means did I expect this to be so involved, even after researching it. But too late now. It works mostly now, please don't rage over how this is all structured. Please email me if there's any questions.

To run the application, you must run the API locally by running fastapi_app.py in a terminal located in the Solitaire_Game_API_new folder

	- Run the command: python fastapi_app.py
	- After running, you should see INFO lines showing up

Note that the application includes continue game and score view. This is NOT ready yet but the base game is funcational.


After starting the server locally, you can run the main application
To do this:
	- Open a prompt in the Lab 4 folder
	- Run the command python lab2_main.py

After this, you can use the application

Before starting a game you must create a username in the server using the menu option 1

After this, you can start a new game using the menu option 2


When playing a game, use the following rules and guides for the layout:

-- EXAMPLE GAME DISPLAY --

Currently playing as: [username]

Foundations:	[C]	[H]	[D]	[S]

Piles:

	[1]	[2]	[3]	[4]	[5]	[6]	[7]	
	[E]	[-]	[-]	[-]	[-]	[-]	[-]
		[E]	[-]	[-]	[-]	[-]	[-]
			[E]	[-]	[-]	[-]	[-]
				[E]	[-]	[-]	[-]
					[E]	[-]	[-]
						[E]	[-]
							[E]



Waste/Draw:	[# of cards in draw]	[E]

User Prompt: [Move/Draw/Show/Cancel Game]


Notes:
[E] --- Any card that is UPWARD facing
[-] --- Any card that is DOWNWARD facing
[C] --- Clubs
[H] --- Hearts
[D] --- Diamonds
[S] --- Spades
[#] --- Pile number



For action prompts, use these strings according to each placement:

[C] -- FOUNDATION_0
[H] -- FOUNDATION_1
[D] -- FOUNDATION_2
[S] -- FOUNDATION_3


[1] -- PILE_0
[2] -- PILE_1
[3] -- PILE_2
[4] -- PILE_3
[5] -- PILE_4
[6] -- PILE_5
[7] -- PILE_6

[DRAW PILE] -- DECK

For card position prompt:
	- To move only one card, use -1
	- To move more cards, use -2, -3, and so on based on the number wanted to move 


