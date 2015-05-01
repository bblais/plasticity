## Summary

Plasticity is a package with a convenient interface, used to run simulations of single cells and networks of neurons. It is used to explore BCM synaptic modification, Hebbian learning, ICA, and others. It accompanies the book Theory of Cortical Plasticity, http://web.bryant.edu/~bblais/plasticity/book.html, by Leon Cooper, Nathan Intrator, Brian Blais, and Harel Shouval. It is available from World Scientific.

This project is supported in part by NSF CRCNS Grant "The Cellular Basis of Receptive Field Plasticity in Visual Cortex: An Integrative, Experimental and Theoretical Approach" #IIS-0515285

The basic principle of the simulations is the presentation of pattern and noise vectors to a network of neurons, with specified lateral connectivity and synaptic modification rule. The pattern vectors are either patches from images or simply read from a pickled .dat file as columns of a matrix. The noise vectors are generated during run-time. The interface lets you specify many things including

* the dimensionality of the inputs
* number of channels (left/right eye, ON/OFF channels, etc.)
* the pattern input files
* generation of input files from a specified correlation function
* the noise mean, variance and type (uniform, gaussian, etc.)
* the lateral connectivity
* the learning rule
* constraints on the weights (normalization, saturation limits, etc.)
* number of neurons
* number of iterations
* what information to display


## Install

To install, just type:

    python setup.py install

To run, either do:

    import plasticity
    plasticity.run()

or

    run the Plasticity.pyw script
