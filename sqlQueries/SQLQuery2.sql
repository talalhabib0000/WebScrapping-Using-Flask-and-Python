Select * from Movies
Select * from Prediction


SELECT MovieID,
(
SELECT Movies.MovieName 
from Movies 
where Movies.MovieID = Prediction.MovieID) as MovieName,
PredictionResult,Percentage,PredictedDate
from Prediction
Group by MovieID,PredictionResult,Percentage,PredictedDate



SELECT MovieID,
(SELECT Movies.MovieName from Movies 
where Movies.MovieID = Prediction.MovieID) as MovieName,PredictionResult,Percentage,PredictedDate from Prediction Group by MovieID,PredictionResult,Percentage,PredictedDate