#program to plot one experiment with and whitout monitor
# To launch it: Rscript plot_monitor.R

autoPlot <- function(array_mo,array_nomo,fileName)
{
  setwd("results/")                     #place the pdf in resuts file
  Name <-paste(fileName, "goap.pdf",sep="-")           #add the pdf instance
  print(c("running",Name))              #beginning of the plot creation
  pdf(Name,width = 8, height = 6)
  
  # Monitor Datas
  colonne <- dim(array_mo)[1]              # recover the number of lines in the csv
  
  # add datas of the first line
  N_frame_mo = c(array_mo[1,1])
  N_goal_reached_mo = c(array_mo[1,11])
  N_death_mo = c(array_mo[1,10])
  Reward_mean_mo = c(array_mo[1,2])
  
  #recover all the data of each line
  for (k in seq(2, colonne)) {
    N_frame_mo = c(N_frame_mo, array_mo[k,1])
    N_goal_reached_mo = c(N_goal_reached_mo, array_mo[k,11])
    N_death_mo = c(N_death_mo, array_mo[k,10])
    Reward_mean_mo = c(Reward_mean_mo, array_mo[k,2])
  }
  
  #No Monitor Data
  colonne <- dim(array_nomo)[1]              # recover the number of lines in the csv
  # add datas of the first line
  N_frame_nomo = c(array_nomo[1,1])
  N_goal_reached_nomo = c(array_nomo[1,11])
  N_death_nomo = c(array_nomo[1,10])
  Reward_mean_nomo = c(array_nomo[1,2])
  #recover all the data of each line
  for (k in seq(2, colonne)) {
    N_frame_nomo = c(N_frame_nomo, array_nomo[k,1])
    N_goal_reached_nomo = c(N_goal_reached_nomo, array_nomo[k,11])
    N_death_nomo = c(N_death_nomo, array_nomo[k,10])
    Reward_mean_nomo = c(Reward_mean_nomo, array_nomo[k,2])
  }
  
  #plot the graph with datas: in red data with monitor and in blue data without monitor
  long=max(max(N_frame_mo),max(N_frame_nomo))
  
  # first graph with N_goal_reached
  max = max(max(N_goal_reached_mo),max(N_goal_reached_nomo))
  min = min(min(N_goal_reached_mo),min(N_goal_reached_nomo))
  plot(N_frame_mo,N_goal_reached_mo, type = 'l', col="red", ylim = c(min,max),xlim=c(0,long), ylab= "")
  lines(N_frame_nomo,N_goal_reached_nomo,type ='l', col="blue")
  legend(1,5,legend = c("N_goal_reached_goap","N_goal_reached_no_goap"), col = c("red","blue"), lty=1:1, cex=0.8)
  
  #second graph with Reward_mean
  max = max(max(N_death_mo),max(N_death_nomo))
  min = min(min(N_death_mo),min(N_death_nomo))
  plot(N_frame_mo,N_death_mo, type = 'l', col="red", ylim = c(min,max),xlim=c(0,long), ylab= "")
  lines(N_frame_nomo,N_death_nomo,type ='l', col="blue")
  legend(1,5,legend = c("N_death_goap","N_death_no_goap"), col = c("red","blue"), lty=1:1, cex=0.8)
  
  #third graph with Reward_mean
  max = max(max(Reward_mean_mo),max(Reward_mean_nomo))
  min = min(min(Reward_mean_mo),min(Reward_mean_nomo))
  plot(N_frame_mo,Reward_mean_mo, type = 'l', col="red", ylim = c(min,max), xlim=c(0,long),ylab= "")
  lines(N_frame_nomo,Reward_mean_nomo,type  ='l', col="blue")
  legend(1,0.7,legend = c("Reward_mean_goap","Reward_mean_no_goap"), col = c("red","blue"), lty=1:1, cex=0.8)
  
  dev.off()                   #Close the pdf
  setwd("..")                 #return in the current directory
  print("It's over")
}

#create the plot for each csv file in evaluation
for (csvFile in Sys.glob("evaluations/dqn*_2_0.csv")){
  #charge the file with no monitor
  not_NaN_in_csv_mo = TRUE
  not_NaN_in_csv_nomo = TRUE
  array = read.csv(csvFile)
  if (dim(array)[1] > 1) {
    for(i in seq(1,length(array))) {
      for(j in seq(1,dim(array)[1])) {
        if (NaN %in% array[j,i]) {
          not_NaN_in_csv_nomo = FALSE
        }
      }
    }
    if (not_NaN_in_csv_nomo) {
      array_nomo = read.csv(csvFile)
      Name_nomo = substr(csvFile,1, nchar(csvFile)-4)      #delete the csv instance
      Name_nomo = substr(Name_nomo,13,nchar(Name_nomo))
    }
  }
  #charge the file with monitor
  csvFile=sub("_2","",csvFile)
  array = read.csv(csvFile)
  if (dim(array)[1] > 1) {
    for(i in seq(1,length(array))) {
      for(j in seq(1,dim(array)[1])) {
        if (NaN %in% array[j,i]) {
          not_NaN_in_csv_mo = FALSE
        }
      }
    }
    if (not_NaN_in_csv_mo) {
      array_mo = read.csv(csvFile)
      Name_mo = substr(csvFile,1, nchar(csvFile)-4)      #delete the csv instance
      Name_mo = substr(Name_mo,13,nchar(Name_mo))
    }
  }
  if (not_NaN_in_csv_mo && not_NaN_in_csv_nomo) {
    autoPlot(array_mo,array_nomo,Name_mo)
  }
}
