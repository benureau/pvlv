# Primary Value and Learned Value Learning Algorithm

[![Binder](http://mybinder.org/badge.svg)](http://mybinder.org:/repo/humm/pvlv)

This repository holds a Python implementation of the Primary Value and Learned
Value Learning Algorithm (PVLV), as described in the [eponymous article](http://ski.clps.brown.edu/papers/OReillyFrankHazyEtAl07.pdf) by
Randall C. O'Reilly, Michael J. Frank, Thomas E. Hazy and Brandon Watz.

The PVLV experiments were originally conducted using the [emergent simulator](https://grey.colorado.edu/emergent), which offers extensive
visualization and interaction possibilities. It uses highly optimized C++
code, which makes it difficult to extract the underlying algorithms from it.
This Python implementation strives to be as simple as possible to understand and
modify, forgoing any optimization ambitions.

This repository includes an implementation of the underlying [Leabra framework](https://grey.colorado.edu/emergent/index.php/Leabra). The Leabra
framework significantly evolved in since the publication of the PVLV article in 2007. Here we reimplement the Leabra framework corresponding to emergent 5.0.

## Online Notebooks

[Notebooks can be run online](http://mybinder.org:/repo/humm/pvlv) through the [mybinder](http://mybinder.org) service.


## Status & Roadmap

- [x] Unit class
- [x] Unit example
- [x] Layer class
- [x] Layer example
- [ ] Network class
- [ ] Network/Layer example
- [ ] PVLV algorithm
- [ ] PVLV example
- [ ] PVLV visualization
- [ ] Results reproduced


## Useful Resources

These resources were instrumental to understand the algorithms and reproduce the results:

  * The original [PVLV: The Primary Value and Learned Value Learning Algorithm](http://ski.clps.brown.edu/papers/OReillyFrankHazyEtAl07.pdf) article.
  * The [CECN1 book](https://grey.colorado.edu/CompCogNeuro/index.php/CECN).
  * The [CECN1 projects](https://grey.colorado.edu/CompCogNeuro/index.php/CECN1_Projects).
  * The [PVLV Pvl Cond project](http://grey.colorado.edu/mediawiki/sites/CompCogNeuro/images/1/18/pvlv_pvlcond.proj) for emergent 5.0.2 (displays errors when used with more recent versions).
  * The Matlab implementation of Leabra by Sergio Verduzco-Flores, available in the `Matlab/` directory of the [emergent source code](https://grey.colorado.edu/emergent).


## License

Open-source, but to be decided.
