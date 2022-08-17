	Create Table 
			Movies 
			(
				MovieID varchar(255) NOT NULL PRIMARY KEY,
				MovieName varchar(255)
			);
	Create Table 
			Prediction 
			(
			MovieID varchar(255) Foreign Key References Movies(MovieID),
			PredictionResult varchar(255),
			PredictedDate Date
			);
			Select * from Prediction
			
		Alter Table Prediction Add PredictedDate Date;
	Create Table 
			Reviews 
			(
			ReviewID varchar(255),
			MovieID varchar(255) Foreign Key References Movies(MovieID), 
			Review varchar
			);

		
			Select * from Movies

			SELECT FORMAT (getdate(), 'MMM dd yyyy') as date

			Insert into Prediction()

			Select * from Prediction

			Insert into Prediction (predictedDate) values ('Select ')


			Select * from PRediction


			Insert into Prediction (PredictedDate) values (GETDATE());

			Select * from movies

			
		

			Select * from Prediction

			Select * from Prediction Join Movies on Movies.MovieID=Prediction.MovieID

			Select * from Prediction

			Select Prediction.MovieID from movies
			join Prediction on 
			Movies.MovieID=Prediction.MovieID



Select * from Prediction


				  select * from Prediction
				  Select * from movies

				  Alter Table prediction 
				  drop constraint FK__Predictio__Movie__3C69FB99

				  Alter Table Prediction
				  add constraint FK_Mov_Prediction_Cascade_Delete
				  foreign key (MovieID) references Movies(MovieID) on delete cascade

				  

				  
				  Select * from Movies


Select  Movies.MovieID,Movies.MovieName,Prediction.PredictionResult, Prediction.PredictedDate from Movies
Join Prediction 
on Movies.MovieID=Prediction.MovieID

Select * from Movies
Select * from Prediction


Select * from Movies 
Union All
Select * from Prediction

Select * from Prediction 

Alter Table Prediction 
Add Percentage int

Select * from Prediction

ALTER TABLE Prediction
DROP COLUMN PredictedDate;

Alter Table Prediction
Add PredictedDate Date


Alter Table Prediction
ALTER COLUMN Percentage int

Delete Movies where MovieID='tt1877830';

Select * from 
Prediction

Select * from Prediction 
WHERE PredictedDate > DATEADD(day, -30, GETDATE())

	USE Movies;
DELETE FROM Prediction
WHERE PredictedDate < DATEADD(day,-30,GETDATE())

Select  Movies.MovieID,
Movies.MovieName,
Prediction.PredictionResult,
Prediction.PredictedDate
from Movies
Join Prediction 
on 
Movies.MovieID=Prediction.MovieID 





Select  Movies.MovieID,Movies.MovieName,Prediction.PredictionResult,Prediction.Percentage,Prediction.PredictedDate, 
CASE WHEN PredictedDate <=  DATEADD(DAY, 30, GETDATE()) 
Then ('Result')
Else 'No Result'
End As UpdatedDate
from Movies
Join Prediction 
on 
Movies.MovieID=Prediction.MovieID 





Where  PredictedDate <  DATEADD(DAY, 30, GETDATE())

select DATEADD(DAY, 30, GETDATE())





Select  *, 
CASE WHEN PredictedDate <=  DATEADD(DAY, 30, GETDATE()) 
Then (
Select  Movies.MovieID,
Movies.MovieName,
Prediction.PredictionResult,
Prediction.PredictedDate
from Movies
Join Prediction 
on 
Movies.MovieID=Prediction.MovieID 
)
Else 'No Result'
End As UpdatedDate
from Movies
Join Prediction 
on 
Movies.MovieID=Prediction.MovieID 


Select  
Movies.MovieID,
Movies.MovieName,
Prediction.PredictionResult,
Prediction.Percentage,
Prediction.PredictedDate,
DATEADD(day, -30, GETDATE()) as LastDate
from Movies
Join Prediction 
on 
Movies.MovieID=Prediction.MovieID 
WHERE 
PredictedDate <= DATEADD(day, 30, GETDATE()) 
OR  
PredictedDate <= DATEADD(month, 1, GETDATE())

Select * from (
Select 
Movies.MovieName,
Prediction.PredictedDate,
PredictionResult,
Prediction.Percentage
from
	(
Select MovieID from Movies group by MovieID
) m
join Prediction on Prediction.MovieID=m.MovieID
)as t


Select *
from(
	Select	 
		MovieName,
		PredictionResult,
		PredictedDate,
		percentage
	from
	(
		Select 
			*
		from Movies group by MovieID,MovieName
	) PredictedResult 
	join 
	Prediction c on c.MovieID = PredictedResult.MovieID 

) as result 