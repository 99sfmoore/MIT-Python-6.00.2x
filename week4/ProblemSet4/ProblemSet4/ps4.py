# 6.00.2x Problem Set 4

import numpy
import random
import pylab
from ps3b import *

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        return random.random() < self.getClearProb()


    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if random.random() < (self.getMaxBirthProb() *(1-popDensity)):
            return SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
        else:
            raise NoChildException()



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.viruses)       


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        self.viruses = [v for v in self.viruses if not v.doesClear()]
        popDensity = float(self.getTotalPop())/self.getMaxPop()
        newViruses = []
        for v in self.viruses:
            try:
                newViruses.append(v.reproduce(popDensity))
            except NoChildException:
                continue
        self.viruses += newViruses
        return self.getTotalPop()


# #
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    virusPop = [0]*300
    for trial in range(numTrials):
        viruses = [SimpleVirus(maxBirthProb,clearProb) for v in range(numViruses)]
        patient = Patient(viruses,maxPop)
        for step in range(300):
            virusPop[step] += patient.update()
    virusPop = [float(x)/numTrials for x in virusPop]  
    pylab.plot(virusPop,label="Simple Virus")
    pylab.xlabel("Timesteps")
    pylab.ylabel("Virus Population")
    pylab.title("Virus Population over Time")
    pylab.legend()
    pylab.show()




#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

        # TODO


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        
        return self.getResistances().get(drug,False)


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        resistant = True
        for drug in activeDrugs:
            resistant = resistant and self.isResistantTo(drug)
        if resistant and random.random() < (self.getMaxBirthProb() * (1-popDensity)):
            childResistances = {}
            for drug, resist in self.getResistances().iteritems():
                if random.random() < self.getMutProb():
                    childResistances[drug] = not resist
                else:
                    childResistances[drug] = resist
            return ResistantVirus(self.getMaxBirthProb(), self.getClearProb(), childResistances, self.getMutProb())
        else:
            raise NoChildException()

            

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.drugs = []
        # TODO


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)


        # TODO


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.drugs
        # TODO


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        return len([v for v in self.viruses if all(v.isResistantTo(drug) for drug in drugResist)])
        # TODO


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        self.viruses = [v for v in self.viruses if not v.doesClear()]
        popDensity = float(self.getTotalPop())/self.getMaxPop()
        newViruses = []
        for v in self.viruses:
            try:
                newViruses.append(v.reproduce(popDensity, self.getPrescriptions()))
            except NoChildException:
                continue
        self.viruses += newViruses
        return self.getTotalPop()



#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, timeBeforeTreatment, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    endVirusPop = [0]*numTrials
    virusPop = [0]*(timeBeforeTreatment+300)
    resistantVPop = [0]*(timeBeforeTreatment+300)
    for trial in range(numTrials):
        viruses = [ResistantVirus(maxBirthProb,clearProb,resistances,mutProb) for v in range(numViruses)]
        patient = TreatedPatient(viruses,maxPop)
        for step in range(timeBeforeTreatment+300):
            if step == 150:
                patient.addPrescription("guttagonol")
            if step == timeBeforeTreatment + 150:
                patient.addPrescription("gimpex")
            # patient.update()
            virusPop[step] += patient.update()
            resistantVPop[step] += patient.getResistPop(["guttagonol"])
        endVirusPop[trial] = patient.getTotalPop()
    # virusPop = [float(x)/numTrials for x in virusPop]  
    # resistantVPop = [float(x)/numTrials for x in resistantVPop]
    # pylab.subplot(2,1,1)
    # pylab.plot(virusPop,label="Total Virus Population")
    # pylab.plot(resistantVPop, label="Guttagonol-resistant virus population")
    # pylab.xlabel("Timesteps")
    # pylab.ylabel("Virus Population")
    # pylab.title("Virus Population over Time")
    # # pylab.legend()
    # pylab.subplot(2,1,2)
    # pylab.hist(endVirusPop)
    # pylab.show()  
    return endVirusPop
    



#
# PROBLEM 1
#        
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """

    for numSteps in [0,75,150,300]:
        vPop = simulationWithDrug(100,1000,0.1,0.05,{"guttagonol":False,"gimpex":False},0.005,numSteps,numTrials)
        mean = numpy.mean(vPop)
        variance = sum((v - mean)**2 for v in vPop)/len(vPop)
        print "numsteps is ",numSteps
        print "numpy variance is ",numpy.var(vPop)
        print "my variance is ", variance

    #     pylab.subplot(4, 1,row)
    #     pylab.hist(vPop, bins = [50,100,200,300,1000])
    #     pylab.title(numSteps)
    #     row += 1
    #     print "number of Steps: ",numSteps
    #     print vPop
    # pylab.plot([0,75,150,300],cured)
    # pylab.plot(variance)
    # pylab.show()
# simulationWithDrug(100,1000,0.1,0.05,{"guttagonol":True},0.005,150,100)
simulationDelayedTreatment(100)

    #     pylab.plot(virusPop,label="Total Virus Population")
    # pylab.plot(resistantVPop, label="Guttagonol-resistant virus population")
    # pylab.xlabel("Timesteps")
    # pylab.ylabel("Virus Population")
    # pylab.title("Virus Population over Time")
    # pylab.legend()
    # pylab.show()







#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    # TODO
