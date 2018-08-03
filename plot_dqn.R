#program to plot one pdf for one csv:
# To launch it: Rscript plot_result.R

autoPlot <- function(N_episode, N_frame,
      Reward_mean_epi, Reward_mean_frm,
      area_top_epi, area_top_frm,
      area_bot_epi, area_bot_frm,
      last_epsilon, N_steps_goal, losses_mean, fileName)
{

  # Create pdf for one csv file
  #:param N_episode: datas for N_episode column
  #:param N_frame: datas for N_frame column
  #:param Reward_mean_epi: datas for Reward_mean column in epi csv
  #:param Reward_mean_frm: datas for Reward_mean column in epi frm
  #:param area_top_epi: positive Reward_mean error from epi_csv
  #:param area_bot_epi: positive Reward_mean error from epi_csv
  #:param area_top_frm: positive Reward_mean error from frm_csv
  #:param area_bot_frm: positive Reward_mean error from frm_csv
  #:param last_epsilon: datas for last_epsilon column
  #:param N_steps_goal: datas for N_steps_goal column
  #:param losses_mean: datas for losses_mean column
  #:param fileName: pdf Name

  setwd("results/")                     #place the pdf in resuts file
  Name <- paste(fileName, ".pdf",sep="")             #add the pdf instance
  print(c("running",Name))              #beginning of the plot creation
  pdf(Name,width = 8, height = 6)

  #plot the graph with datas
  # first graph with N_frame in X axis and Reward_mean in Y axis
  max = max(area_top_frm)
  min = min(area_bot_frm)
  plot(N_frame, Reward_mean_frm,type = 'l', col = "blue", ylab = "", ylim = c(min,max))
  polygon(c(N_frame, rev(N_frame)), c(area_top_frm, rev(area_bot_frm)), col = "skyblue", border = NA, density = 65)
  legend(1,0.03,legend = c("Reward_mean"), col = c("blue"), lty=1:1, cex=0.8)
  
  # second graph with N_frame in X axis and losses_mean in Y axis
  plot(N_frame, losses_mean, type = 'l', col = "blue", ylab = "")
  legend(2000,1000000,legend = c("losses_mean"), col = c("blue"), lty=1:1, cex=0.8)
  
  #third graph with with N_Episode in X axis and Reward_mean in Y axis
  max = max(area_top_epi)
  min = min(area_bot_epi)
  plot(N_episode, Reward_mean_epi, type = 'l', col = "blue", ylab = "", ylim = c(min,max))
  polygon(c(N_episode, rev(N_episode)), c(area_top_epi, rev(area_bot_epi)), col = "skyblue", border = NA, density = 65)
  legend(1,0.04,legend = c("Reward_mean"), col = c("blue"), lty=1:1, cex=0.8)

  #fourth graph with with N_Episode in X axis and last_epsilon in Y axis
  plot(N_episode, last_epsilon, type = 'l', col = "blue")
  legend(10,0.5,legend = c("last_epsilon"), col = c("blue"), lty=1:1, cex=0.8)

  #fifth graph with with N_Episode in X axis and N_steps_goal in Y axis
  plot(N_episode, N_steps_goal, type = 'l', col = "blue")
  legend(100,2000,legend = c("N_steps_goal"), col = c("blue"), lty=1:1, cex=0.8)

  dev.off()                   #Close the pdf
  setwd("..")                 #return in the current directory
  print("It's over")
}

autoPlot_five <- function(N_episode, N_frame,
                          Reward_mean_epi, Reward_mean_frm,
                          last_epsilon, N_steps_goal, losses_mean, list_Name, number_of_csv, PdfName)
{

  # Create pdf for 2 to 5 csv
  #:param N_episode: list datas for N_episode columns
  #:param N_frame: list datas for N_frame columns
  #:param Reward_mean_epi: list datas for Reward_mean columns in epi csv
  #:param Reward_mean_frm: list datas for Reward_mean column in epi frm
  #:param last_epsilon: list datas for last_epsilon columns
  #:param N_steps_goal: list datas for N_steps_goal columns
  #:param losses_mean: list datas for losses_mean columns
  #:param list_Name: list of csv Name
  #:param number_of_plot: number of csv to plot
  #:param PdfName: pdf Name

  setwd("results/")                     #place the pdf in resuts file
  print(c("running several csv",PdfName))              #beginning of the plot creation
  pdf(PdfName,width = 8, height = 6)

  color_array <- c("blue", "red", "green", "yellow", "brown")
  # recover the longer number of episode
  long_episode <- lapply(N_episode[1], function(x) x[which.max(abs(x))])
  for(i in seq(2, number_of_csv)) {
    if ( as.double(lapply(N_episode[i], function(x) x[which.max(abs(x))])) > as.double(long_episode)) {
      long_episode= lapply(N_episode[i], function(x) x[which.max(abs(x))])
    }
  }
  long_episode <- as.double(long_episode)

  # recover the longer number of frame
  long_frame = lapply(N_frame[1], function(x) x[which.max(abs(x))])
  for(i in seq(2, number_of_csv)) {
    if (as.double(lapply(N_frame[i], function(x) x[which.max(abs(x))])) > as.double(long_frame)) {
      long_frame = lapply(N_frame[i], function(x) x[which.max(abs(x))])
    }
  }
  long_frame = as.double(long_frame)


  # first graph with N_frame in X axis and Reward_mean in Y axis
  # recover the Y maximum value
  max = lapply(Reward_mean_frm[1], function(x) x[which.max(abs(x))])
  for(i in seq(2, number_of_csv)) {
    if(as.double(lapply(Reward_mean_frm[i], function(x) x[which.max(abs(x))]))>as.double(max)) {
      max = lapply(Reward_mean_frm[i], function(x) x[which.max(abs(x))])
    }
  }
  max = as.double(max)
  plot(unlist(N_frame[1]), unlist(Reward_mean_frm[1]), type = 'l', col = color_array[1], xlab = "N_frame", ylab = "Reward_mean_frm",
      xlim = c(0, long_frame), ylim = c(- max, max))
  if (number_of_csv > 1) {
    for(i in seq(2, number_of_csv)) {
      lines(unlist(N_frame[i]), unlist(Reward_mean_frm[i]), type = 'l', col = color_array[i])
    }
  }
  legend(1, 0.03, legend = list_Name, col = color_array, lty=1:1, cex=0.8)


  # second graph with N_frame in X axis and losses_mean in Y axis
  # recover the Y maximum value
  max = lapply(losses_mean[1], function(x) x[which.max(abs(x))])
  for(i in seq(2, number_of_csv)) {
    if (as.double(lapply(losses_mean[i], function(x) x[which.max(abs(x))])) > as.double(max)) {
      max = lapply(losses_mean[i], function(x) x[which.max(abs(x))])
    }
  }
  max = as.double(max)
  plot(unlist(N_frame[1]), unlist(losses_mean[1]), type = 'l', col = color_array[1], xlab = "N_frame", ylab = "losses_mean",
      xlim = c(0, long_frame), ylim = c(0, max))
  if (number_of_csv > 1) {
    for(i in seq(2, number_of_csv)) {
      lines(unlist(N_frame[i]), unlist(losses_mean[i]), type = 'l', col = color_array[i])
    }
  }
  legend(2000, 500000, legend = list_Name, col = color_array, lty=1:1, cex=0.8)


  # third graph with N_episode in X axis and Reward_mean in Y axis
  # recover the Y maximum value
  max = lapply(Reward_mean_epi[1], function(x) x[which.max(abs(x))])
  for(i in seq(2, number_of_csv)) {
    if (as.double(lapply(Reward_mean_epi[i], function(x) x[which.max(abs(x))])) > as.double(max)) {
      max = lapply(Reward_mean_epi[i], function(x) x[which.max(abs(x))])
    }
  }
  max = as.double(max)
  plot(unlist(N_episode[1]), unlist(Reward_mean_epi[1]), type = 'l', col = color_array[1], xlab = "N_frame", ylab = "Reward_mean_epi",
      xlim = c(0, long_episode), ylim = c(- max, max))
  if (number_of_csv > 1) {
    for(i in seq(2, number_of_csv)) {
      lines(unlist(N_episode[i]), unlist(Reward_mean_epi[i]), type = 'l', col = color_array[i])
    }
  }
  legend(1, 0.04, legend = list_Name, col = color_array, lty=1:1, cex=0.8)


  # fourth graph with N_episode in X axis and last_epsilon in Y axis
  # recover the Y maximum value
  max = lapply(last_epsilon[1], function(x) x[which.max(abs(x))])
  for(i in seq(2, number_of_csv)) {
    if (as.double(lapply(last_epsilon[i], function(x) x[which.max(abs(x))])) > as.double(max)) {
      max = lapply(last_epsilon[i], function(x) x[which.max(abs(x))])
    }
  }
  max <- as.double(max)
  plot(unlist(N_episode[1]), unlist(last_epsilon[1]), type = 'l', col = color_array[1], xlab = "N_episode", ylab = "last_epsilon",
      xlim = c(0, long_episode), ylim = c(0, max))
  if (number_of_csv > 1) {
    for(i in seq(2, number_of_csv)) {
      lines(unlist(N_episode[i]), unlist(last_epsilon[i]),type = 'l', col = color_array[i])
    }
  }
  legend(10, 0.5, legend = list_Name, col = color_array, lty=1:1, cex=0.8)


  # recover the Y maximum value
  # fifth graph with N_episode in X axis and N_steps_goal in Y axis
  max = lapply(N_steps_goal[1], function(x) x[which.max(abs(x))])
  for(i in seq(2, number_of_csv)) {
    if (as.double(lapply(N_steps_goal[i], function(x) x[which.max(abs(x))])) > as.double(max)) {
      max = lapply(N_steps_goal[i], function(x) x[which.max(abs(x))])
    }
  }
  max = as.double(max)
  plot(unlist(N_episode[1]), unlist(N_steps_goal[1]), type = 'l', col = color_array[1], xlab = "N_episode", ylab = "N_steps_goal",
      xlim = c(0, long_episode), ylim = c(0, max))
  if (number_of_csv > 1) {
    for(i in seq(2, number_of_csv)) {
      lines(unlist(N_episode[i]), unlist(N_steps_goal[i]),type = 'l', col = color_array[i])
    }
  }
  legend(100, 2000, legend = list_Name, col = color_array, lty=1:1, cex=0.8)

  dev.off()                   #Close the pdf
  setwd("..")                 #return in the current directory
  print("It's over")
}


# count the number of functions are call
number_of_plot_five <- 0
number_of_plot <- 0

# create variables who stock the data of each csv
N_episode_list <- c()
Reward_mean_epi_list <- c()
last_epsilon_list <- c()
N_steps_goal_list <- c()

N_frame_list <- c()
Reward_mean_frm_list <- c()
losses_mean_list <- c()

list_Name <- c()
long_list <- cbind(rbind(0, 0), rbind(0, 0), rbind(0, 0), rbind(0, 0), rbind(0, 0))



#create the plot for each csv file in evaluation
for (csvFile in Sys.glob("evaluations/dqn_epi*.csv")){
  # the file don't test to plot csv with less than line of datas or with NaN (Not a Number)
  not_NaN_in_csv_epi = TRUE
  not_NaN_in_csv_frm = TRUE
  #extract the datas in epi csv
  array_epi = read.csv(csvFile)
  if (dim(array_epi)[1] > 1) {
    for(i in seq(1,length(array_epi))) {
      for(j in seq(1,dim(array_epi)[1])) {
        if (NaN %in% array_epi[j,i]) {
          not_NaN_in_csv_epi = FALSE
        }
      }
    }
    if (not_NaN_in_csv_epi) {
      Name = substr(csvFile,1, nchar(csvFile)-4)      #delete the csv instance
      Name = substr(Name,13, nchar(Name))
    }
  }
  else {
    not_NaN_in_csv_epi = FALSE
  }
  # extract datas in frm csv
  csvFile=sub("epi","frm",csvFile)
  array_frm = read.csv(csvFile)
  if (dim(array_frm)[1] > 1) {
    for(i in seq(1,length(array_frm))) {
      for(j in seq(1,dim(array_frm)[1])) {
        if (NaN %in% array_frm[j,i]) {
          not_NaN_in_csv_frm = FALSE
        }
      }
    }
  }
  else {
    not_NaN_in_csv_frm = FALSE
  }

  if (not_NaN_in_csv_epi &&  not_NaN_in_csv_frm) {
    # add datas of the first line (epi_csv)
    N_episode <- c(array_epi[1,1])
    Reward_mean_epi <- c(array_epi[1, 2])
    Reward_sem_epi <- c(array_epi[1, 6])
    area_top_epi <- Reward_mean_epi
    area_bot_epi <- Reward_mean_epi
    last_epsilon <- c(array_epi[1, 12])
    N_steps_goal <- c(array_epi[1, 13])


    #recover all the data of each line (epi_csv)
    for (k in seq(2, dim(array_epi)[1])) {
      N_episode <- c(N_episode, array_epi[k,1])
      Reward_mean_epi <- c(Reward_mean_epi, array_epi[k, 2])
      Reward_sem_epi = c(Reward_sem_epi, array_epi[k, 6])
      area_top_epi <- c(area_top_epi, Reward_mean_epi[k] +
                                          Reward_sem_epi[k - 1])
      area_bot_epi <- c(area_bot_epi, Reward_mean_epi[k] -
                                          Reward_sem_epi[k - 1])
      last_epsilon <- c(last_epsilon, array_epi[k, 12])
      N_steps_goal <- c(N_steps_goal, array_epi[k, 13])
    }


    # add datas of the first line (frm_csv)
    N_frame <- c(array_frm[1,1])
    Reward_mean_frm <- c(array_frm[1, 2])
    Reward_sem_frm <- c(array_frm[1, 6])
    area_top_frm <- Reward_mean_frm
    area_bot_frm <- Reward_mean_frm
    losses_mean <- c(array_frm[1, 8])


    #recover all the data of each line (frm_csv)
    for (k in seq(2, dim(array_frm)[1])) {
      N_frame <- c(N_frame, array_frm[k,1])
      Reward_mean_frm <- c(Reward_mean_frm, array_frm[k, 2])
      Reward_sem_frm <- c(Reward_sem_frm, array_frm[k, 6])
      area_top_frm <- c(area_top_frm, Reward_mean_frm[k] + Reward_sem_frm[k - 1])
      area_bot_frm <- c(area_bot_frm, Reward_mean_frm[k] - Reward_sem_frm[k - 1])
      losses_mean <- c(losses_mean, array_frm[k, 8])
    }


    # call the function which plot each graphical curve (single csv)
    autoPlot(N_episode, N_frame,
      Reward_mean_epi, Reward_mean_frm,
      area_top_epi, area_top_frm,
      area_bot_epi, area_bot_frm,
      last_epsilon, N_steps_goal, losses_mean, Name)

    number_of_plot <- number_of_plot + 1


    # stock the data of the csv for plot several csv in one time
    N_episode_list  <- c(N_episode_list, N_episode)
    N_frame_list  <- c(N_frame_list, N_frame)
    Reward_mean_epi_list <- c(Reward_mean_epi_list, Reward_mean_epi)
    Reward_mean_frm_list <- c(Reward_mean_frm_list, Reward_mean_frm)
    last_epsilon_list <- c(last_epsilon_list, last_epsilon)
    N_steps_goal_list <- c(N_steps_goal_list, N_steps_goal)
    losses_mean_list <- c(losses_mean_list, losses_mean)

    list_Name <- c(list_Name, Name)
    long_list[1, number_of_plot] <- dim(array_epi)[1]
    long_list[2, number_of_plot] <- dim(array_frm)[1]
  }



  if (number_of_plot == 5 ) {           # if 5 csv are plot
    # Create the list to send to function who crete the pdf whit several curve
    list_episode <- list(N_episode_list[1 : long_list[1, 1]], N_episode_list[long_list[1, 1] + 1 : long_list[1, 2]],
                        N_episode_list[long_list[1, 1] + long_list[1, 2] + 1 : long_list[1, 3]],
                        N_episode_list[long_list[1, 1] + long_list[1, 2] + long_list[1, 3] + 1 : long_list[1, 4]],
                        N_episode_list[long_list[1, 1] + long_list[1, 2] + long_list[1, 3] + long_list[1, 4]+ 1 : long_list[1, 5]])
    list_frame <- list(N_frame_list[1 : long_list[2, 1]], N_frame_list[long_list[2, 1] + 1 : long_list[2, 2]],
                        N_frame_list[long_list[2, 1] + long_list[2, 2] + 1 : long_list[2, 3]],
                        N_frame_list[long_list[2, 1] + long_list[2, 2] + long_list[2, 3] + 1 : long_list[2, 4]],
                        N_frame_list[long_list[2, 1] + long_list[2, 2] + long_list[2, 3] + long_list[2, 4]+ 1 : long_list[2, 5]])
    list_reward_mean_epi <- list(Reward_mean_epi_list[1 : long_list[1, 1]], Reward_mean_epi_list[long_list[1, 1] + 1 : long_list[1, 2]],
                        Reward_mean_epi_list[long_list[1, 1] + long_list[1, 2] + 1 : long_list[1, 3]],
                        Reward_mean_epi_list[long_list[1, 1] + long_list[1, 2] + long_list[1, 3] + 1 : long_list[1, 4]])
    list_reward_mean_frm <- list(Reward_mean_frm_list[2 : long_list[2, 1]], Reward_mean_frm_list[long_list[2, 1] + 1 : long_list[2, 2]],
                        Reward_mean_frm_list[long_list[2, 1] + long_list[2, 2] + 1 : long_list[2, 3]],
                        Reward_mean_frm_list[long_list[2, 1] + long_list[2, 2] + long_list[2, 3] + 1 : long_list[2, 4]],
                        Reward_mean_frm_list[long_list[2, 1] + long_list[2, 2] + long_list[2, 3] + long_list[2, 4]+ 1 : long_list[2, 5]])
    list_last_epsilon <- list(last_epsilon_list[1 : long_list[1, 1]], last_epsilon_list[long_list[1, 1] + 1 : long_list[1, 2]],
                        last_epsilon_list[long_list[1, 1] + long_list[1, 2] + 1 : long_list[1, 3]],
                        last_epsilon_list[long_list[1, 1] + long_list[1, 2] + long_list[1, 3] + 1 : long_list[1, 4]])
    list_steps_goal <- list(N_steps_goal_list[1 : long_list[1, 1]], N_steps_goal_list[long_list[1, 1] + 1 : long_list[1, 2]],
                        N_steps_goal_list[long_list[1, 1] + long_list[1, 2] + 1 : long_list[1, 3]],
                        N_steps_goal_list[long_list[1, 1] + long_list[1, 2] + long_list[1, 3] + 1 : long_list[1, 4]])
    list_losses_mean <- list(losses_mean_list[1 : long_list[2, 1]], losses_mean_list[long_list[2, 1] + 1 : long_list[2, 2]],
                        losses_mean_list[long_list[2, 1] + long_list[2, 2] + 1 : long_list[2, 3]],
                        losses_mean_list[long_list[2, 1] + long_list[2, 2] + long_list[2, 3] + 1 : long_list[2, 4]],
                        losses_mean_list[long_list[2, 1] + long_list[2, 2] + long_list[2, 3] + long_list[2, 4]+ 1 : long_list[2, 5]])
  #Name of the pdf: "dqn_csv_several_number_of_plot_five.pdf"
  PdfName <- "dqn_csv_several"
  PdfName <- paste(PdfName, number_of_plot_five,sep="_")
  PdfName <- paste(PdfName, ".pdf",sep="")
  # call the function who create one pdf with several csv
  autoPlot_five(list_episode, list_frame,
                list_reward_mean_epi, list_reward_mean_frm,
                list_last_epsilon, list_steps_goal, list_losses_mean, list_Name, number_of_plot, PdfName)
    number_of_plot <- 0
    number_of_plot_five <- number_of_plot_five + 1
  }
}



if (number_of_plot > 1 || number_of_plot != 5) {  # Create a last pdf with last csvFiles (several csv)
  # Create the list to send to the function
  list_episode <- list(N_episode_list[1 : long_list[1, 1]], N_episode_list[long_list[1, 1] + 1 : long_list[1, 2]],
                        N_episode_list[long_list[1, 1] + long_list[1, 2] + 1 : long_list[1, 3]],
                        N_episode_list[long_list[1, 1] + long_list[1, 2] + long_list[1, 3] + 1 : long_list[1, 4]])
  list_frame <- list(N_frame_list[1 : long_list[2, 1]], N_frame_list[long_list[2, 1] + 1 : long_list[2, 2]],
                        N_frame_list[long_list[2, 1] + long_list[2, 2] + 1 : long_list[2, 3]],
                        N_frame_list[long_list[2, 1] + long_list[2, 2] + long_list[2, 3] + 1 : long_list[2, 4]])
  list_reward_mean_epi <- list(Reward_mean_epi_list[1 : long_list[1, 1]], Reward_mean_epi_list[long_list[1, 1] + 1 : long_list[1, 2]],
                        Reward_mean_epi_list[long_list[1, 1] + long_list[1, 2] + 1 : long_list[1, 3]],
                        Reward_mean_epi_list[long_list[1, 1] + long_list[1, 2] + long_list[1, 3] + 1 : long_list[1, 4]])
  list_reward_mean_frm <- list(Reward_mean_frm_list[1 : long_list[2, 1]], Reward_mean_frm_list[long_list[2, 1] + 1 : long_list[2, 2]],
                        Reward_mean_frm_list[long_list[2, 1] + long_list[2, 2] + 1 : long_list[2, 3]],
                        Reward_mean_frm_list[long_list[2, 1] + long_list[2, 2] + long_list[2, 3] + 1 : long_list[2, 4]])
  list_last_epsilon <- list(last_epsilon_list[1 : long_list[1, 1]], last_epsilon_list[long_list[1, 1] + 1 : long_list[1, 2]],
                        last_epsilon_list[long_list[1, 1] + long_list[1, 2] + 1 : long_list[1, 3]],
                        last_epsilon_list[long_list[1, 1] + long_list[1, 2] + long_list[1, 3] + 1 : long_list[1, 4]])
  list_steps_goal <- list(N_steps_goal_list[1 : long_list[1, 1]], N_steps_goal_list[long_list[1, 1] + 1 : long_list[1, 2]],
                        N_steps_goal_list[long_list[1, 1] + long_list[1, 2] + 1 : long_list[1, 3]],
                        N_steps_goal_list[long_list[1, 1] + long_list[1, 2] + long_list[1, 3] + 1 : long_list[1, 4]])
  list_losses_mean <- list(losses_mean_list[1 : long_list[2, 1]], losses_mean_list[long_list[2, 1] + 1 : long_list[2, 2]],
                        losses_mean_list[long_list[2, 1] + long_list[2, 2] + 1 : long_list[2, 3]],
                        losses_mean_list[long_list[2, 1] + long_list[2, 2] + long_list[2, 3] + 1 : long_list[2, 4]])
  #Name of the pdf: "dqn_csv_several_number_of_plot_five.pdf"
  PdfName <- "dqn_csv_several"
  PdfName <- paste(PdfName, number_of_plot_five,sep="_")
  PdfName <- paste(PdfName, ".pdf",sep="")
  # call the function who create one pdf with several csv
  autoPlot_five(list_episode, list_frame,
                list_reward_mean_epi, list_reward_mean_frm,
                list_last_epsilon, list_steps_goal, list_losses_mean, list_Name, number_of_plot, PdfName)
}