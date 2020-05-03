import numpy as np
import matplotlib.pyplot as plt

class Community:

  # initalization method
  def __init__(self, name, space_size):

    self.name = name # name of the community
    self.space = np.zeros((space_size,space_size)) # numpy array that represents the physical space
    self.population = self.space.size # the size of the population
    self.susceptible = self.space.size # the current number of healthy people in the population
    self.infected = 0 # the current number of infected people in the population
    self.recovered = 0 # the current number of infected people in the population
    self.snapshots = [] # this will contain numpy arrays that represent each time step
    self.SIR = np.zeros((3,1)) #this contains a time series of the number of susceptible, infected, recovered
    self.time = np.zeros(1) # this array will be the time array
    self.base_infection_probability = 0 # this is the base infection probability
    self.infection_probability = 0 # this is the infection probability applied to all the population in this community
    self.recovery_probability = 0 # this is the probability of recovering if the person is infected
    self.peak_number_of_infections = 0 # this is the peak number of infected people at the same time during the simulation
    self.total_infections = 0 # this is the total number of people that were infected or are currently infected at the time where the outbreak ends
    self.duration_of_outbreak = 0 # this is the number of time steps that the outbreaks lasts, calculated to be the 
                                  # time step after the peak where the number of infected is for the first time less 
                                  # than 10% of the peak number of infected 

  def resetSimulatedData(self):
    self.space = 0*self.space # numpy array that represents the physical space
    self.susceptible = self.space.size # the current number of healthy people in the population
    self.infected = 0 # the current number of infected people in the population
    self.recovered = 0 # the current number of infected people in the population
    self.snapshots = [] # this will contain numpy arrays that represent each time step
    self.SIR = np.zeros((3,1)) #this contains a time series of the number of susceptible, infected, recovered
    self.time = np.zeros(1) # this array will be the time array

  # method to add the initially infected
  def addInitiallyInfected(self, number_initially_infected):

    x_infected = 0
    y_infected = 0
    
    # place as many infected as required in this loop
    while self.infected < number_initially_infected:
        
        # randomly generate the position
        x_infected = np.random.randint(0,self.space.shape[0])
        y_infected = np.random.randint(0,self.space.shape[1])
        
        # check that the position isn't already occupied by an infected
        if (self.space[x_infected][y_infected] == 0):
            self.space[x_infected][y_infected] = 1
            self.infected += 1
    
    # add the initial values of healthy/infected to the arrays keeping track
    self.SIR[0, 0] = self.getSusceptible()
    self.SIR[1, 0] = self.getInfected()

    # add the first snapshot of the simulation
    self.snapshots.append(self.getSpace().copy())


  # method that simulates one time step
  def simulateOneTimeStep(self):
    self.susceptibleToInfected()
    self.infectedToRecovered()
    
    # add the new values of healthy/infected/recovered to the arrays keeping track
    SIR_t = np.array([self.getSusceptible(), self.getInfected(), self.getRecovered()])
    #update SIR time series
    self.SIR = np.concatenate([self.SIR, SIR_t[:,np.newaxis]], axis=1)

    # add the new snapshot of the simulation
    self.snapshots.append(self.getSpace().copy())
    
  def susceptibleToInfected(self):

    #create a mask to sieve those uninfected out
    infected = self.space == 1

    # add extra boundaries
    expan1 = np.hstack((infected,np.zeros((self.space.shape[0],1))))
    expan1 = np.vstack((expan1,np.zeros((1,expan1.shape[1]))))
    expan1 = np.hstack((np.zeros((expan1.shape[0],1)),expan1))
    expan1 = np.vstack((np.zeros((1,expan1.shape[1])),expan1))

    # make the addition for how many infected are around each position
    expan2 = (expan1[:-2,:-2] + 
              expan1[:-2,1:-1] + 
              expan1[:-2,2:] + 
              expan1[1:-1,2:] + 
              expan1[2:,2:] + 
              expan1[2:,1:-1] + 
              expan1[2:,0:-2] + 
              expan1[1:-1,0:-2])
    
    exposedToRisk = np.logical_and(expan2 > 0, self.space == 0)
    # initialize a random matrix where around infection_probability % of the values are True
    infect_prob_arr = np.random.rand(self.space.shape[0], self.space.shape[1]) < self.infection_probability
    # find the overlap between healthy and 
    self.space[np.logical_and(exposedToRisk, infect_prob_arr)] = 1

  def infectedToRecovered(self):
    # initialize a random matrix where around recovery_probability % of the values are True
    recover_prob_arr = np.random.rand(self.space.shape[0],self.space.shape[1]) < self.recovery_probability
    # find the overlap between infected and above array and make those people recovered
    self.space[np.logical_and(self.space == 1, recover_prob_arr)] = 2

  # method that performs a consecutive number of time steps in our simulation

  # get methods
  def getSpace(self):
    return self.space

  def getName(self):
    return self.name

  def getPopulation(self):
    return self.population

  def getSusceptible(self):

    # use a mask and sum it to see the number of healthy people, designated as having a value equal to zero
    self.susceptible = np.sum((self.getSpace()) == 0)
    
    return self.susceptible

  def getInfected(self):

    # use a mask and sum it to see the number of infected people, designated as having a value equal to one
    self.infected = np.sum((self.getSpace()) == 1)

    return self.infected

  def getRecovered(self):

    # use a mask and sum it to see the number of recovered people, designated as having a value equal to two
    self.recovered = np.sum((self.getSpace()) == 2)

    return self.recovered


  # set methods
  def setBaseInfectionProbability(self, probability):
    self.base_infection_probability = probability

  def calculateInfectionProbability(self, r):
    self.infection_probability = self.base_infection_probability * (1 - r)

  def setRecoveryProbability(self, probability):
    self.recovery_probability = probability





class Simulator():

  def __init__(self, communitiesDict):

    self.communitiesDict = communitiesDict
    self.resultsDict = {}

    for name in communitiesDict.keys():
      self.resultsDict[name] = {'max_infected_array': np.zeros(0),
                                'total_infected_array': np.zeros(0),
                                'duration_array': np.zeros(0)}

  def multipleTimeSteps(self, num_timesteps, plot=False):
    for tp in np.arange(num_timesteps):
      pass
  
  def migrationSimulationofTwoCommunities(self, com1, com2, numSwapped, simulationSteps, plot=False):
    for _ in np.arange(simulationSteps):
        swapIndices = np.random.permutation(com1.population)[:numSwapped]
        com1xswap, com1yswap = swapIndices // com1.space.shape[0], swapIndices % com1.space.shape[1]

        swapIndices2= np.random.permutation(com2.population)[:numSwapped]
        com2xswap, com2yswap = swapIndices2 // com2.space.shape[0], swapIndices2 % com2.space.shape[1]

        #tmp = com2.space[com2xswap, com2yswap]

        #if com1.population > com2.population:
        tmp = com1.space[com1xswap, com1yswap]

        com1.space[com1xswap, com1yswap] = com2.space[com2xswap, com2yswap]
        com2.space[com2xswap, com2yswap] = tmp
    
        com1.simulateOneTimeStep()
        com2.simulateOneTimeStep()

    # # append the maximum number of infected at a single time step
    # com1['max_infected_array'] = np.append(com1.['max_infected_array'], self.communitiesDict[name].peak_number_of_infections)
    # com2['max_infected_array'] = np.append(com2.['max_infected_array'], self.communitiesDict[name].peak_number_of_infections)  

    # # append the duration of the outbreak
    # com1['duration_array'] = np.append(com1.['duration_array'], 
    #                                                          self.communitiesDict[name].duration_of_outbreak)
    # com2['duration_array'] = np.append(com2.['duration_array'], 
    #                                                          self.communitiesDict[name].duration_of_outbreak)

    # # append the total number of people that are or were infected at the time step where the outbreak ends
    # com1['total_infected_array'] = np.append(com1.['total_infected_array'], 
    #                                                                self.communitiesDict[name].total_infections)
    # com2['total_infected_array'] = np.append(com2.['total_infected_array'], 
    #                                                                self.communitiesDict[name].total_infections)
    #counter=1
    #print(counter, end=' ')
    #counter += 1

    com1.time = np.arange(simulationSteps+1)
    com2.time = np.arange(simulationSteps+1)

    if plot:
      fig, (ax1, ax2) = plt.subplots(2, sharex=True)
      fig.suptitle('Time (in units of time)')
      ax1.scatter(com1.time, com1.SIR[0], label='healthy')
      ax1.scatter(com1.time, com1.SIR[1], label='infected')
      ax1.scatter(com1.time, com1.SIR[2], label='recovered')

      ax2.scatter(com2.time, com2.SIR[0], label='healthy')
      ax2.scatter(com2.time, com2.SIR[1], label='infected')
      ax2.scatter(com2.time, com2.SIR[2], label='recovered')

      ax1.grid()
      ax2.grid()
      ax1.legend()
      ax2.legend()

      ax1.set_title('Community 1')
      ax2.set_title('Community 2')
      plt.show()

  def multipleSimulationsOfSameSIRScenario(self, simulationSteps, numberOfSimulations, initiallyInfected=1, plot=False):
    """
    Uses the same community to simulate the same scenario multiple times
    and keeps track of the max number of infected during the entire
    simulation.
    """
    counter = 1

    for name in self.communitiesDict.keys():
      
      self.communitiesDict[name].time = np.arange(simulationSteps)
      for n in np.arange(numberOfSimulations):
        # clear the simulated data in the Community
        self.communitiesDict[name].resetSimulatedData()
        
        # add initially infected
        self.communitiesDict[name].addInitiallyInfected(initiallyInfected)

        # make the simulation
        for _ in np.arange(simulationSteps):
          self.communitiesDict[name].simulateOneTimeStep()

        # append the maximum number of infected at a single time step
        self.resultsDict[name]['max_infected_array'] = np.append(self.resultsDict[name]['max_infected_array'], self.communitiesDict[name].peak_number_of_infections) 

        # append the duration of the outbreak
        self.resultsDict[name]['duration_array'] = np.append(self.resultsDict[name]['duration_array'], 
                                                             self.communitiesDict[name].duration_of_outbreak)

        # append the total number of people that are or were infected at the time step where the outbreak ends
        self.resultsDict[name]['total_infected_array'] = np.append(self.resultsDict[name]['total_infected_array'], 
                                                                   self.communitiesDict[name].total_infections)

        print(counter, end=' ')
        counter += 1
        #print(str(n + 1), end=' ')

        self.communitiesDict[name].time = np.arange(simulationSteps+1)
        if plot:
          plt.scatter(self.communitiesDict[name].time, self.communitiesDict[name].SIR[0,:], label='infected')
          plt.scatter(self.communitiesDict[name].time, self.communitiesDict[name].SIR[1,:], label='recovered')
          plt.scatter(self.communitiesDict[name].time, self.communitiesDict[name].SIR[2,:], label='healthy')
          plt.title(name)
          plt.grid()
          plt.legend()
          plt.show()

    