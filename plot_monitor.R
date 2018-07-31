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
  N_step_mo = c(array_mo[1,2])
  N_step_AVG_mo = c(array_mo[1,16])
  N_goal_reached_mo = c(array_mo[1,15])
  N_death_mo = c(array_mo[1,17])
  Reward_mean_mo = c(array_mo[1,4])
  #recover all the data of each line
  for (k in seq(2, colonne)) {
    N_step_mo = c(N_step_mo, array_mo[k,2])
    N_step_AVG_mo = c(N_step_AVG_mo, array_mo[k,16])
    N_goal_reached_mo = c(N_goal_reached_mo, array_mo[k,15])
    N_death_mo = c(N_death_mo, array_mo[k,17])
    Reward_mean_mo = c(Reward_mean_mo, array_mo[k,4])
  }

  #No Monitor Data
  colonne <- dim(array_nomo)[1]              # recover the number of lines in the csv
  # add datas of the first line
  N_step_nomo = c(array_nomo[1,2])
  N_step_AVG_nomo = c(array_nomo[1,16])
  N_goal_reached_nomo = c(array_nomo[1,15])
  N_death_nomo = c(array_nomo[1,17])
  Reward_mean_nomo = c(array_nomo[1,4])
  #recover all the data of each line
  for (k in seq(2, colonne)) {
    N_step_nomo = c(N_step_nomo, array_nomo[k,2])
    N_step_AVG_nomo = c(N_step_AVG_nomo, array_nomo[k,16])
    N_goal_reached_nomo = c(N_goal_reached_nomo, array_nomo[k,15])
    N_death_nomo = c(N_death_nomo, array_nomo[k,17])
    Reward_mean_nomo = c(Reward_mean_nomo, array_nomo[k,4])
  }

  #plot the graph with datas: in red data with monitor and in blue data without monitor
  long=max(max(N_step_mo),max(N_step_nomo))
  # first graph with N_step_AVG:
  max = max(max(N_step_AVG_mo),max(N_step_AVG_nomo))
  min = min(min(N_step_AVG_mo),min(N_step_AVG_nomo))
  plot(N_step_mo,N_step_AVG_mo, type = 'l', col="red", ylim=c(min,max),xlim=c(0,long), ylab= "")
  lines(N_step_nomo,N_step_AVG_nomo,type ='l', col="blue")
  legend(1,80,legend = c("N_step_AVG_goap","N_step_AVG_no_goap"), col = c("red","blue"), lty=1:1, cex=0.8)

  # second graph with N_goal_reached
  max = max(max(N_goal_reached_mo),max(N_goal_reached_nomo))
  min = min(min(N_goal_reached_mo),min(N_goal_reached_nomo))
  plot(N_step_mo,N_goal_reached_mo, type = 'l', col="red", ylim = c(min,max),xlim=c(0,long), ylab= "")
  lines(N_step_nomo,N_goal_reached_nomo,type ='l', col="blue")
  legend(1,30,legend = c("N_goal_reached_goap","N_goal_reached_no_goap"), col = c("red","blue"), lty=1:1, cex=0.8)

  #third graph with Reward_mean
  max = max(max(N_death_mo),max(N_death_nomo))
  min = min(min(N_death_mo),min(N_death_nomo))
  plot(N_step_mo,N_death_mo, type = 'l', col="red", ylim = c(min,max),xlim=c(0,long), ylab= "")
  lines(N_step_nomo,N_death_nomo,type ='l', col="blue")
  legend(1,30,legend = c("N_death_goap","N_death_no_goap"), col = c("red","blue"), lty=1:1, cex=0.8)

  #fourth graph with Reward_mean
  max = max(max(Reward_mean_mo),max(Reward_mean_nomo))
  min = min(min(Reward_mean_mo),min(Reward_mean_nomo))
  plot(N_step_mo,Reward_mean_mo, type = 'l', col="red", ylim = c(min,max), xlim=c(0,long),ylab= "")
  lines(N_step_nomo,Reward_mean_nomo,type  ='l', col="blue")
  legend(1,0.7,legend = c("Reward_mean_goap","Reward_mean_no_goap"), col = c("red","blue"), lty=1:1, cex=0.8)

  dev.off()                   #Close the pdf
  setwd("..")                 #return in the current directory
  print("It's over")
}


N_whitout_mo = 0
N_whit_mo = 0
N_total_death_nomo = 0
N_total_death_mo = 0
N_death_by_end_nomo = 0
N_death_by_end_mo = 0
N_death_env_nomo = 0
N_death_env_mo = 0

N_saved_nomo = 0
N_saved_mo = 0

N_episode_nomo = 0
N_episode_mo = 0
N_steps_nomo = 0
N_steps_mo = 0
N_Updates_nomo = 0
N_Updates_mo = 0

#create the plot for each csv file in evaluation
for (csvFile in Sys.glob("evaluations/*_2.csv")){
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
      N_whitout_mo = N_whitout_mo + 1
      N_total_death_nomo = N_total_death_nomo + array[dim(array)[1], 20]
      N_death_by_end_nomo = N_death_by_end_nomo + array[dim(array)[1], 19]
      N_death_env_nomo = N_death_env_nomo + array[dim(array)[1], 17]
      N_saved_nomo = N_saved_nomo + array[dim(array)[1], 18]
      N_episode_nomo = N_episode_nomo + array[dim(array)[1], 21]
      N_steps_nomo = N_steps_nomo + array[dim(array)[1], 2]
      N_Updates_nomo = N_Updates_nomo + array[dim(array)[1], 1]
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
      N_whit_mo = N_whit_mo + 1
      N_total_death_mo = N_total_death_mo + array[dim(array)[1], 20]
      N_death_by_end_mo = N_death_by_end_mo + array[dim(array)[1], 19]
      N_death_env_mo = N_death_env_mo + array[dim(array)[1], 17]
      N_saved_mo = N_saved_mo + array[dim(array)[1], 18]
      N_episode_mo = N_episode_mo + array[dim(array)[1], 21]
      N_steps_mo = N_steps_mo + array[dim(array)[1], 2]
      N_Updates_mo = N_Updates_mo + array[dim(array)[1], 1]
      array_mo = read.csv(csvFile)
      Name_mo = substr(csvFile,1, nchar(csvFile)-4)      #delete the csv instance
      Name_mo = substr(Name_mo,13,nchar(Name_mo))
    }
  }
  if (not_NaN_in_csv_mo && not_NaN_in_csv_nomo) {
    autoPlot(array_mo,array_nomo,Name_mo)
  }
}
                          # call the function which plot each graphical curve

N_total_death_mo = N_total_death_mo / N_whit_mo
N_death_by_end_mo = N_death_by_end_mo / N_whit_mo
N_death_env_mo = N_death_env_mo / N_whit_mo
N_saved_mo = N_saved_mo / N_whit_mo
N_episode_mo = N_episode_mo / N_whit_mo
N_steps_mo = N_steps_mo / N_whit_mo
N_Updates_mo = N_Updates_mo / N_whit_mo

N_total_death_nomo = N_total_death_nomo / N_whitout_mo
N_death_by_end_nomo = N_death_by_end_nomo / N_whitout_mo
N_death_env_nomo = N_death_env_nomo / N_whitout_mo
N_saved_nomo = N_saved_nomo / N_whitout_mo
N_episode_nomo = N_episode_nomo / N_whitout_mo
N_steps_nomo = N_steps_nomo / N_whitout_mo
N_Updates_nomo = N_Updates_nomo / N_whitout_mo

# print all the mean info
print("Goap Data: ")
print(c("N_total_death : ", N_total_death_mo, "  N_death_by_end : ", N_death_by_end_mo, "  N_death_by_Environment : ", N_death_env_mo))
print(c("N_saved : ", N_saved_mo))
print(c("N_Episodes", N_episode_mo, "  N_steps : ", N_steps_mo, "  N_Updates : ", N_Updates_mo))

print("                            ")
print("No Goap Data: ")
print(c("N_total_death : ", N_total_death_nomo, "  N_death_by_end : ", N_death_by_end_nomo, "  N_death_by_Environment : ", N_death_env_nomo))
print(c("N_saved : ", N_saved_nomo))
print(c("N_Episodes", N_episode_nomo, "  N_steps : ", N_steps_nomo, "  N_Updates : ", N_Updates_nomo))
