	Create Table 
			Movies 
			(
				MovieID int NOT NULL PRIMARY KEY,
				MovieName varchar(255)
			);
	Create Table 
			Prediction 
			(
			MovieID int, Foreign Key (MovieID) References Movies(MovieID),
			Prediction varchar(255),
			PredictedDate Date
			);
	Create Table 
			Reviews 
			(
			MovieID int,
			Foreign Key (MovieID) References Movies(MovieID), 
			Review varchar
			);



			Select @@SERVERNAME


			Insert into 