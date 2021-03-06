# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (15,5)

class Community:
    """ 
    A class used to a community of individuals.


    Attributes
    ----------
    name : String
        String that represents the name of this community.
    
    space : numpy array
        A 2D numpy array that represents all the individuals in the community.
    
    population : int
        The size of the population.

    susceptible : int
        The number of susceptible people in the current state of the Community.
    
    infected : int
        The number of infected people in the current state of the Community.
    
    recovered : int
        The number of recovered people in the current state of the Community.
    
    snapshots : list
        List of 2D numpy arrays that represent the space at each step of the 
        simulation.
    
    SIR : numpy array
        2D Numpy array that contains the number of susceptible, infected and 
        recovered people in all the time steps of the simulation.
    
    time : numpy array
        1D Numpy array that represents the time steps of the simulation.
    
    base_infection_probability : float
        The base infection probability.
    
    infection_probability : float
        The infection probability after taking into consideration other factors.
        This is the one used in the simulaitons.
    
    recovery_probability : float
        The recovery probability.

    peak_number_of_infections : int
        This is the largest number simultaneously infected during the simulation.
    
    total_infections : int
        This is the number of people that were infected at any point during the
        simulation.
    

    Methods
    -------
    resetSimulatedData()
        If a simulation has been run, then all of the simulated data is stored
        in the Community instance. This method allows reset the simulated data.
        This includes setting the space all equal to zero (all population is
        susceptible), making the number of susceptible people equal to the 
        population, setting both the numbers of infected and recovered people 
        equal to zero, cleaning the snapshots' list, and making both the SIR and
        time numpy arrays the same as in the moment of initialization.
    
    addInitiallyInfected(number_initially_infected)
        Set a number of initially infected people randomly scattered through
        the community.
    
    simulateOneTimeStep()
        Advances the simulation by one step, and updates the SIR and time arrays.

    susceptibleToInfected()
        While advancing the simulation by one step, this method performs the 
        conversion from susceptible to infected.
    
    infectedToRecovered()
        While advancing the simulation by one step, this method performs the
        conversion from infected to recovered.
    
    getSpace()
        Returns the 2D numpy array representing the population.
    
    getName()
        Returns the name of the community.

    getPopulation()
        Returns the population size.
    
    getSusceptible()
        Calculates the number of susceptibles from the current state of the space,
        updates such number and returns it.
    
    getInfected()
        Calculates the number of infected from the current state of the space,
        updates such number and returns it.
    
    getRecovered()
        Calculates the number of recovered from the current state of the space,
        updates such number and returns it.

    setBaseInfectionProbability(probability)
        Sets the base infection probability.
    
    calculateInfectionProbability(r)
        Calculates the infection probability by taking into account the effects
        of counter measures that reduce the base infection probability by r.
    
    setRecoveryProbability(probability)
        Sets the recovery probability.

    """

    # initalization method
    def __init__(self, name, pop_sqrt):
        """
        Parameters
        ----------
        name : String
            String that represents the name of this community.
        
        pop_sqrt : int
            Integer which is the square root of the desired population size.
        """

        self.name = name # name of the community
        self.space = np.zeros((pop_sqrt,pop_sqrt)) # numpy array that represents the physical space
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

    def resetSimulatedData(self):
        """If a simulation has been run, then all of the simulated data is stored
        in the Community instance. This method allows reset the simulated data.
        This includes setting the space all equal to zero (all population is
        susceptible), making the number of susceptible people equal to the 
        population, setting both the numbers of infected and recovered people 
        equal to zero, cleaning the snapshots' list, and making both the SIR and
        time numpy arrays the same as in the moment of initialization.

        """
        self.space = 0*self.space # numpy array that represents the physical space
        self.susceptible = self.space.size # the current number of healthy people in the population
        self.infected = 0 # the current number of infected people in the population
        self.recovered = 0 # the current number of infected people in the population
        self.snapshots = [] # this will contain numpy arrays that represent each time step
        self.SIR = np.zeros((3,1)) #this contains a time series of the number of susceptible, infected, recovered
        self.time = np.zeros(1) # this array will be the time array
        self.total_infections = 0 # set the number of total infections back to zero

    # method to add the initially infected
    def addInitiallyInfected(self, number_initially_infected):
        """Set a number of initially infected people randomly scattered through
        the community.

        Parameters
        ----------
        number_initially_infected : int
            The number of initially infected people in the population.

        """

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
        """Advances the simulation by one step, and updates the SIR and time 
        arrays.

        """

        self.susceptibleToInfected()
        self.infectedToRecovered()

        # add the new values of healthy/infected/recovered to the arrays keeping track
        SIR_t = np.array([self.getSusceptible(), self.getInfected(), self.getRecovered()])
        #update SIR time series
        self.SIR = np.concatenate([self.SIR, SIR_t[:,np.newaxis]], axis=1)

        # add the new snapshot of the simulation
        self.snapshots.append(self.getSpace().copy())
    
    def susceptibleToInfected(self):
        """While advancing the simulation by one step, this method performs the 
        conversion from susceptible to infected.

        """

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
        """While advancing the simulation by one step, this method performs the
        conversion from infected to recovered.

        """

        # initialize a random matrix where around recovery_probability % of the values are True
        recover_prob_arr = np.random.rand(self.space.shape[0],self.space.shape[1]) < self.recovery_probability
        # find the overlap between infected and above array and make those people recovered
        self.space[np.logical_and(self.space == 1, recover_prob_arr)] = 2


    # get methods
    def getSpace(self):
        """ Returns the 2D numpy array representing the population.

        Returns
        -------
        space : numpy 2D array
            The current state of the community.

        """
        return self.space

    def getName(self):
        """Returns the name of the community.

        Returns
        -------
        name : str
            The comunnity's name.

        """

        return self.name

    def getPopulation(self):
        """Returns the size of the population.

        Returns
        -------
        population : int
            The comunnity's population.

        """

        return self.population

    def getSusceptible(self):
        """Calculates the number of susceptible from the current state of the space,
        updates such number and returns it.

        Returns
        -------
        susceptible : int
            The comunnity's population that is susceptible.

        """

        # use a mask and sum it to see the number of healthy people, designated as having a value equal to zero
        self.susceptible = np.sum((self.getSpace()) == 0)

        return self.susceptible

    def getInfected(self):
        """Calculates the number of infected from the current state of the space,
        updates such number and returns it.

        Returns
        -------
        infected : int
            The comunnity's population that is infected.

        """

        # use a mask and sum it to see the number of infected people, designated as having a value equal to one
        self.infected = np.sum((self.getSpace()) == 1)

        return self.infected

    def getRecovered(self):
        """Calculates the number of recovered from the current state of the space,
        updates such number and returns it.

        Returns
        -------
        recovered : int
            The comunnity's population that is recovered.

        """

        # use a mask and sum it to see the number of recovered people, designated as having a value equal to two
        self.recovered = np.sum((self.getSpace()) == 2)

        return self.recovered


    # set methods
    def setBaseInfectionProbability(self, probability):
        """Sets the base infection probability.

        Parameters
        ----------
        probability : float
            The probability used as the base infection probability.

        """

        self.base_infection_probability = probability

    def calculateInfectionProbability(self, r):
        """Calculates the infection probability to be used to advance the 
        simulation. To do so, it subtracts r from the base infection probability.

        Parameters
        ----------
        r : float
            The amount to subtract from the probability.

        """

        self.infection_probability = self.base_infection_probability * (1 - r)

    def setRecoveryProbability(self, probability):
        """Sets the recovery probability.

        Parameters
        ----------
        probability : float
            The probability used as the recovery probability.

        """

        self.recovery_probability = probability


class Simulator():
    """ 
    A class used perform multiple simulations on several different communities
    and store results in an organized manner.


    Attributes
    ----------
    communitiesDict : dict
        A python dictionary where the keys are the communities' names, and 
        the values are Community's instances. These are the communities
        where the simulations are going to be run with.
    
    resultsDict : dict
        A python dictionary where the keys are the communities' names, and
        the values are the dictionaries containing the results of all the
        different simulations. These result dictionaries have two keys:
        'max_infected_array' which is a numpy array with the peak number
        of infections of every single simulation run with that Community, 
        and 'total_infected_array' which is also a numpy array with the 
        total number of people that are infectios or where infections at 
        some point during the simulated time.
    

    Methods
    -------
    simulate(self, numberOfSimulations, simulationSteps, initiallyInfected=1, plot=False):
        Perfomrs the inicated number of simulations throughout all the communities 
        in the dictionary of communities. 

    """

    def __init__(self, communitiesDict):
        """
        Parameters
        ----------
        communitiesDict : dict
            A python dictionary where the keys are the communities' names, and 
            the values are Community's instances. These are the communities
            where the simulations are going to be run with.

        """

        # assign the dictionary of communites 
        self.communitiesDict = communitiesDict

        # create the dictionary of results, and populate it.
        self.resultsDict = {}

        for name in communitiesDict.keys():
            self.resultsDict[name] = {'max_infected_array': np.zeros(0),
                                      'total_infected_array': np.zeros(0)}

        # ADD AN AVERAGE SIR CURVE


    def simulate(self, numberOfSimulations, simulationSteps, initiallyInfected=1, plot=False):
        """Perfomrs the inicated number of simulations throughout all the 
        communities in the dictionary of communities. 

        Parameters
        ----------
        numberOfSimulations: int
            The total number of simulations to be performed with each Community.
        simulationSteps : int
            The number of total steps in the simulations.
        initiallyInfected : int, optional
            The initial number of infected people in each simulation. The default
            value is set to 1.
        plot : bool, optional
            Boolean to indicate if the SIR plots should be displayed. Defaul value
            is set to False.

        """

        # make a loop to go through all the communities.
        for name in self.communitiesDict.keys():

            for n in np.arange(numberOfSimulations):

                # make sure that the community is reset
                self.communitiesDict[name].resetSimulatedData()

                # assign the simulation time for the community.
                self.communitiesDict[name].time = np.arange(simulationSteps + 1)


                # add initially infected
                self.communitiesDict[name].addInitiallyInfected(initiallyInfected)

                # perform a single simulation for each community
                for _ in np.arange(simulationSteps):
                    self.communitiesDict[name].simulateOneTimeStep()
                
                # update the max number of infected and append the result
                self.communitiesDict[name].peak_number_of_infections = np.max(self.communitiesDict[name].SIR[1:])

                self.resultsDict[name]['max_infected_array'] = np.append(self.resultsDict[name]['max_infected_array'], 
                                                                        self.communitiesDict[name].peak_number_of_infections) 


                # append the total number of people that are or were infected at the time step where the outbreak ends
                self.communitiesDict[name].total_infections = self.communitiesDict[name].getRecovered() + self.communitiesDict[name].getInfected()

                self.resultsDict[name]['total_infected_array'] = np.append(self.resultsDict[name]['total_infected_array'], 
                                                                        self.communitiesDict[name].total_infections)
                
                # create the plot
                if plot:
                    plt.scatter(self.communitiesDict[name].time, self.communitiesDict[name].SIR[0,:], label='Susceptible', s=5)
                    plt.scatter(self.communitiesDict[name].time, self.communitiesDict[name].SIR[1,:], label='Infectious', s=5)
                    plt.scatter(self.communitiesDict[name].time, self.communitiesDict[name].SIR[2,:], label='Recovered', s=5)
                    plt.title(name)
                    plt.grid()
                    plt.legend()
                    plt.show()