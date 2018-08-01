#program to plot one pdf for one csv:
# To launch it: Rscript plot_result.R

autoPlot <- function(array,fileName)
{
  setwd("results/")                     #place the pdf in resuts file
  Name <-paste(fileName, ".pdf",sep="")             #add the pdf instance
  print(c("running",Name))              #beginning of the plot creation
  pdf(Name,width = 8, height = 6)
  
  colonne <- dim(array)[1]              # recover the number of lines in the csv
  
  # add datas of the first line
  N_frame = c(array[1,1])
  N_goal_reached = c(array[1,11])
  N_death = c(array[1,10])
  Reward_mean = c(array[1,2])
  
  #recover all the data of each line
  for (k in seq(2, colonne)) {
    N_frame = c(N_frame, array[k,1])
    N_goal_reached = c(N_goal_reached, array[k,11])
    N_death = c(N_death, array[k,10])
    Reward_mean = c(Reward_mean, array[k,2])
  }
  
  #plot the graph with datas
  # first graph with N_step_AVG and N_goal_reached
  plot(N_frame,N_goal_reached,type ='l', col="red", ylab="")
  legend(1,5,legend = c("N_goal_reached"), col = c("red"), lty=1:1, cex=0.8)
  
  # second graph with N_saved and N_death
  plot(N_frame,N_death,type ='l', col="red",ylab="")
  legend(1,5,legend = c("N_death"), col = c("red"), lty=1:1, cex=0.8)
  
  #third graph with Reward_mean and Reward_std
  plot(N_frame,Reward_mean, type = 'l', col="red")
  legend(1,0.7,legend = c("Reward_mean"), col = c("red"), lty=1:1, cex=0.8)
  
  dev.off()                   #Close the pdf
  setwd("..")                 #return in the current directory
  print("It's over")
}


#create the plot for each csv file in evaluation
for (csvFile in Sys.glob("evaluations/dqn*.csv")){
  # the file don't test to plot csv with less than line of datas or with NaN (Not a Number)
  not_NaN_in_csv = TRUE
  array = read.csv(csvFile)
  if (dim(array)[1] > 1) {
    for(i in seq(1,length(array))) {
      for(j in seq(1,dim(array)[1])) {
        if (NaN %in% array[j,i]) {
          not_NaN_in_csv = FALSE
        }
      }
    }
    if (not_NaN_in_csv) {
      Name = substr(csvFile,1, nchar(csvFile)-4)      #delete the csv instance
      Name = substr(Name,13, nchar(Name))
      autoPlot(array,Name)                            # call the function which plot each graphical curve
    }
  }
}
