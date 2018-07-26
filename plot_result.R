#program to plot one pdf for one csv:
# To launch it: Rscript plot_result.R

autoPlot <- function(array,fileName)
{
  setwd("results/")                     #place the pdf in resuts file
  Name <- c(fileName,".pdf")            #add the pdf instance
  print(c("running",Name))              #beginning of the plot creation
  pdf(Name,width = 8, height = 6)
  
  colonne <- dim(array)[1]              # recover the number of lines in the csv

  # add datas of the first line
  N_step = c(array[1,2])
  N_step_AVG = c(array[1,16])
  N_goal_reached = c(array[1,15])
  N_death = c(array[1,17])
  N_saved = c(array[1,18])
  Reward_mean = c(array[1,4])
  Reward_std = c(array[1,8])
  #recover all the data of each line
  for (k in seq(2, colonne)) {
     N_step = c(N_step, array[k,2])
     N_step_AVG = c(N_step_AVG, array[k,16])
     N_goal_reached = c(N_goal_reached, array[k,15])
     N_death = c(N_death, array[k,17])
     N_saved = c(N_saved, array[k,18])
     Reward_mean = c(Reward_mean, array[k,4])
     Reward_std = c(Reward_std, array[k,8])
  }


  #plot the graph with datas
  # first graph with N_step_AVG and N_goal_reached
  max = max(max(N_step_AVG),max(N_goal_reached))
  min = min(min(N_step_AVG),min(N_goal_reached))
  plot(N_step,N_step_AVG, type = 'l', col="red", ylim=c(min - 0.1,max + 0.1), ylab= "")
  lines(N_step,N_goal_reached,type ='l', col="blue")
  legend(1,80,legend = c("N_step_AVG","N_goal_reached"), col = c("red","blue"), lty=1:1, cex=0.8)

  # second graph with N_saved and N_death
  max = max(max(N_saved),max(N_death))
  min = min(min(N_saved),min(N_death))
  plot(N_step,N_saved, type = 'l', col="red", ylim = c(min -0.1,max +0.1), ylab= "")
  lines(N_step,N_death,type ='l', col="blue")
  legend(1,30,legend = c("N_saved","N_death"), col = c("red","blue"), lty=1:1, cex=0.8)

  #third graph with Reward_mean and Reward_std
  max = max(max(Reward_mean),max(Reward_std))
  min = min(min(Reward_mean),min(Reward_std))
  plot(N_step,Reward_mean, type = 'l', col="red", ylim = c(min - 0.1,max + 0.1), ylab= "")
  lines(N_step,Reward_std,type  ='l', col="blue")
  legend(1,0.7,legend = c("Reward_mean","Reward_std"), col = c("red","blue"), lty=1:1, cex=0.8)

  dev.off()                   #Close the pdf
  setwd("..")                 #return in the current directory
  print("It's over")
}

#create the plot for each csv file in evaluation
for (csvFile in Sys.glob("evaluations/*.csv")){
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
