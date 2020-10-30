students <- read.csv("/home/jack/edudata/R_df.csv",
                     header = TRUE,
                     na.strings=c("", "NA"),
                     sep = ",")

library(ggplot2)
str(students)

ggplot(dat4, aes(x = Student, y = Time)) + 
  theme_bw() +
  theme(panel.grid.major = element_line(colour = "#d3d3d3"),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(), panel.background = element_blank(),
        plot.title = element_text(size = 14, family = "Tahoma", face = "bold"),
        text=element_text(family="Tahoma"),
        axis.title = element_text(face="bold"),
        axis.text.x=element_text(colour="black", size = 11),
        axis.text.y=element_text(colour="black", size = 9),
        axis.line = element_line(size=0.5, colour = "black")) +
  geom_boxplot(outlier.colour='RED', outlier.size=3) + 
  scale_y_continuous(name = "Time spent (Seconds)") +
  scale_x_discrete(name = "Student (First 3 characters of username)") +
  ggtitle("Distribution of time spent by each student on each milestone") +
  geom_text(aes(label=outlier), na.rm=TRUE, nudge_y = 40)


boxplot(students)
dat4 <- students %>% tibble::rownames_to_column(var="outlier") %>% group_by(Student) %>% mutate(is_outlier=ifelse(is_outlier(Time), Time, as.numeric(NA)))
dat4$outlier[which(is.na(dat4$is_outlier))] <- as.numeric(NA)

dat4 <- edit(dat4)

students2 <- read.csv("/home/jack/milestone logging/R_df2.csv",
                     header = TRUE,
                     na.strings=c("", "NA"),
                     sep = ",")
library(dplyr)
library(tibble)

is_outlier <- function(x) {
  return(x < quantile(x, 0.25) - 1.5 * IQR(x) | x > quantile(x, 0.75) + 1.5 * IQR(x))
}



dat <- students2 %>% tibble::rownames_to_column(var="outlier") %>% group_by(Student) %>% mutate(is_outlier=ifelse(is_outlier(Attempts), Attempts, as.numeric(NA)))
dat$outlier[which(is.na(dat$is_outlier))] <- as.numeric(NA)
dat <- edit(dat)

ggplot(dat, aes(x = Student, y = Attempts)) + 
  theme_bw() +
  theme(panel.grid.major = element_line(colour = "#d3d3d3"),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(), panel.background = element_blank(),
        plot.title = element_text(size = 14, family = "Tahoma", face = "bold"),
        text=element_text(family="Tahoma"),
        axis.title = element_text(face="bold"),
        axis.text.x=element_text(colour="black", size = 11),
        axis.text.y=element_text(colour="black", size = 9),
        axis.line = element_line(size=0.5, colour = "black")) +
  scale_y_continuous(name = "Number of attempts") +
  geom_boxplot(outlier.colour='RED', outlier.size=3) + 
  scale_x_discrete(name = "Student (First 3 characters of username)") +
  ggtitle("Distribution of number of attempts by each student on each milestone") + 
  geom_text(aes(label=outlier), na.rm=TRUE, nudge_y = 1)

dat2 <- dat
dat2 <- edit(dat2)

dat2 <- students2 %>% tibble::rownames_to_column(var="outlier") %>% group_by(Milestone) %>% mutate(is_outlier=ifelse(is_outlier(Attempts), Attempts, as.numeric(NA)))
dat2$outlier[which(is.na(dat2$is_outlier))] <- as.numeric(NA)

ggplot(dat2, aes(x = Milestone, y = Attempts)) + 
  theme_bw() +
  theme(panel.grid.major = element_line(colour = "#d3d3d3"),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(), panel.background = element_blank(),
        plot.title = element_text(size = 14, family = "Tahoma", face = "bold"),
        text=element_text(family="Tahoma"),
        axis.title = element_text(face="bold"),
        axis.text.x=element_text(colour="black", size = 11),
        axis.text.y=element_text(colour="black", size = 9),
        axis.line = element_line(size=0.5, colour = "black")) +
  scale_y_continuous(name = "Number of attempts") +
  geom_boxplot(outlier.colour='RED', outlier.size=3) + 
  scale_x_discrete(name = "Milestone #") +
  ggtitle("Distribution of number of attempts at each milestone") + 
  geom_text(aes(label=outlier), na.rm=TRUE, nudge_y = .5)

students2 <- edit(students2)
