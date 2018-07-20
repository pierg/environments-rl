#program to plot one experiment with and whitout monitor
# To launch it: Rscript plot_monitor.R

autoPlot <- function(array_mo,array_nomo,fileName)
{
  setwd("results/")                     #place the pdf in resuts file
  Name <- c(fileName,".pdf")            #add the pdf instance
  print(c("running",Name))              #beginning of the plot creation
  pdf(Name,width = 8, height = 6)
  
  # Monitor Datas
  colonne <- dim(array_mo)[1]              # recover the number of lines in the csv
  # add datas of the first line 
  N_step_mo = c(array_mo[1,2])
  N_step_AVG_mo = c(array_mo[1,16])
  N_goal_reached_mo = c(array_mo[1,15])
  Reward_mean_mo = c(array_mo[1,4])
  #recover all the data of each line
  for (k in seq(2, colonne)) {
    N_step_mo = c(N_step_mo, array_mo[k,2])
    N_step_AVG_mo = c(N_step_AVG_mo, array_mo[k,16])
    N_goal_reached_mo = c(N_goal_reached_mo, array_mo[k,15])
    Reward_mean_mo = c(Reward_mean_mo, array_mo[k,4])
  }
  
  #No Monitor Data
  colonne <- dim(array_nomo)[1]              # recover the number of lines in the csv
  # add datas of the first line 
  N_step_nomo = c(array_nomo[1,2])
  N_step_AVG_nomo = c(array_nomo[1,16])
  N_goal_reached_nomo = c(array_nomo[1,15])
  Reward_mean_nomo = c(array_nomo[1,4])
  #recover all the data of each line
  for (k in seq(2, colonne)) {
    N_step_nomo = c(N_step_nomo, array_nomo[k,2])
    N_step_AVG_nomo = c(N_step_AVG_nomo, array_nomo[k,16])
    N_goal_reached_nomo = c(N_goal_reached_nomo, array_nomo[k,15])
    Reward_mean_nomo = c(Reward_mean_nomo, array_nomo[k,4])
  }
  
  #plot the graph with datas: in red data with monitor and in blue data without monitor
  long=max(max(N_step_mo),max(N_step_nomo))
  # first graph with N_step_AVG:
  max = max(max(N_step_AVG_mo),max(N_step_AVG_nomo))
  min = min(min(N_step_AVG_mo),min(N_step_AVG_nomo))
  plot(N_step_mo,N_step_AVG_mo, type = 'l', col="red", ylim=c(min,max),xlim=c(0,long), ylab= "")
  lines(N_step_nomo,N_step_AVG_nomo,type ='l', col="blue")
  legend(1,80,legend = c("N_step_AVG_monitor","N_step_AVG_no_monitor"), col = c("red","blue"), lty=1:1, cex=0.8)
  
  # second graph with N_goal_reached
  max = max(max(N_goal_reached_mo),max(N_goal_reached_nomo))
  min = min(min(N_goal_reached_mo),min(N_goal_reached_nomo))
  plot(N_step_mo,N_goal_reached_mo, type = 'l', col="red", ylim = c(min,max),xlim=c(0,long), ylab= "")
  lines(N_step_nomo,N_goal_reached_nomo,type ='l', col="blue")
  legend(1,30,legend = c("N_goal_reached_monitor","N_goal_reached_no_monitor"), col = c("red","blue"), lty=1:1, cex=0.8)
  
  #third graph with Reward_mean
  max = max(max(Reward_mean_mo),max(Reward_mean_nomo))
  min = min(min(Reward_mean_mo),min(Reward_mean_nomo))
  plot(N_step_mo,Reward_mean_mo, type = 'l', col="red", ylim = c(min,max), xlim=c(0,long),ylab= "")
  lines(N_step_nomo,Reward_mean_nomo,type  ='l', col="blue")
  legend(1,0.7,legend = c("Reward_mean_monitor","Reward_mean_no_monitor"), col = c("red","blue"), lty=1:1, cex=0.8)
  
  dev.off()                   #Close the pdf
  setwd("..")                 #return in the current directory
  print("It's over")
}


#create the plot for each csv file in evaluation
for (csvFile in Sys.glob("evaluations/*_2_0.csv")){
  #charge the file with no monitor
  array_nomo = read.csv(csvFile)
  Name_nomo = substr(csvFile,1, nchar(csvFile)-4)      #delete the csv instance
  Name_nomo = substr(Name_nomo,13,nchar(Name_nomo))
  #charge the file with monitor
  csvFile=sub("_2","",csvFile)
  array_mo = read.csv(csvFile)
  Name_mo = substr(csvFile,1, nchar(csvFile)-4)      #delete the csv instance
  Name_mo = substr(Name_mo,13,nchar(Name_mo))
  
  autoPlot(array_mo,array_nomo,Name_mo)                            # call the function which plot each graphical curve
}