
'''
Provides Parametric Standard class, and some specific instances. The
specific instances are named as follows
        StandardType_UnknownQuantity
'''
import numpy as npy
from copy import copy,deepcopy


class ParameterBoundsError(Exception):
    pass

class ParametricStandard(object):
    global INF
    INF=1e12
    '''
    A parametric standard represents a calibration standard which
    has uncertainty in its response. This uncertainty is functionally
    known, and represented by a parametric function, where the
    uknown quantity is the adjustable parameter.

    This class presents an abstract interface to a general Parametric
    Standard. Its main purpose is to allow the self calibration routine
    to be independent of calibration set.

    See initializer for more
    details.
    '''
    def __init__(self, function=None, parameters={}, parameter_bounds={},**kwargs):
        '''
        takes:
                function: a function which will be called to generate
                        a Network type, to be used as a ideal response.

                parameters: an dictionary holding an list of parameters,
                        which will be the dependent variables to optimize.
                        these are passed to the network creating function.

                **kwargs: keyword arguments passed to the function, but
                        not used in parametric optimization.
        '''
        self.kwargs = kwargs
        self.parameters = parameters
        self.function = function
        self.parameter_bounds = parameter_bounds

    @property
    def parameter_keys(self):
        '''
        returns a list of parameter dictionary keys in alphabetical order
        '''
        keys = self.parameters.keys()
        keys.sort()
        return keys

    @property
    def parameter_array(self):
        '''
        This property provides a 1D-array interface to the parameters
        dictionary. This is needed to intereface teh optimizing function
        because it only takes a 1D-array. Therefore, order must be
        preserved with accessing and updating the parameters through this
        array. To handle this I make it return and update in alphebetical
        order of the parameters dictionary keys.
        '''
        return npy.array([self.parameters[k] for  k in self.parameter_keys])

    @parameter_array.setter
    def parameter_array(self,input_array):
        counter = 0
        for k in self.parameter_keys:
            self.parameters[k]= input_array[counter]
            counter+=1

    @property
    def parameter_bounds_array(self):
        '''
        This property provides a 1D-array interface to the parameters
        bounds dictionary. if key doesnt exist, then i presume the
        parameter has no bounds. this then returns a tuple of -INF,INF
        where INF is a global variable in this class.
        '''
        return ([self.parameter_bounds.get(k,(-INF,INF)) for  k in self.parameter_keys])


    @property
    def number_of_parameters(self):
        '''
        the number of parameters this standard has
        '''
        return len(self.parameter_keys)

    @property
    def s(self):
        '''
        a direct access to the calulated networks' s-matrix
        '''
        return self.network.s

    @property
    def network(self):
        '''
         a Networks instance generated by calling self.function(), for
        the current set of parameters (and kwargs)
        '''
        tmp_args = copy(self.kwargs)
        tmp_args.update(self.parameters)

        #for k in range( self.number_of_parameters):
            #if not(self.parameter_bounds_array[k][0] < self.parameter_array[k] \
            #       <self.parameter_bounds_array[k][1]):
            #       raise ParameterBoundsError('a parameter is out of bounds')

        return self.function(**tmp_args)







## multi-standards
class SlidingLoad_UnknownTermination(ParametricStandard):
    '''
    A set of parametersized standards representing a set of Delayed
     Terminations of known length, but unknown termination
    '''

    def __init__(self, media,d_list,Gamma0,**kwargs):
        '''
        takes:
                media: a Media type, with a RectangularWaveguide object
                        for its tline property.
                d_list: list of distances to termination [m]
                Gamma0: guess for reflection coefficient off termination at
                        termination
                **kwargs: passed to self.function
        '''
        raise (NotImplementedError())
        kwargs.update({'Gamma0':Gamma0,})

        #def tempfunc(Gamma0,**kwargs):
        #
            #return [media.delay_load(


        parameters = {}
        #[parameters['d'+str(k)] = d_list[k] for k in range(len(d_list))]
        ParametricStandard.__init__(self, \
                function = media.delay_load,\
                parameters = parameters,\
                **kwargs\
                )
