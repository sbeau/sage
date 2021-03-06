r"""
Associahedron

.. TODO::

    - fix adjacency matrix
    - edit graph method to get proper vertex labellings
    - UniqueRepresentation?

AUTHORS:

- Christian Stump
"""
#*****************************************************************************
#       Copyright (C) 2011-2012 Christian Stump <christian.stump@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from sage.geometry.polyhedron.backend_ppl import Polyhedron_QQ_ppl
from sage.geometry.polyhedron.parent import Polyhedra_QQ_ppl
from sage.combinat.root_system.cartan_type import CartanType
from sage.modules.free_module_element import vector
from sage.rings.all import QQ


def Associahedron(cartan_type):
    r"""
    Construct an associahedron.

    The generalized associahedron is a polytopal complex with vertices in
    one-to-one correspondence with clusters in the cluster complex, and with
    edges between two vertices if and only if the associated two clusters
    intersect in codimension 1.

    The associahedron of type `A_n` is one way to realize the classical
    associahedron as defined in the :wikipedia:`Associahedron`.

    A polytopal realization of the associahedron can be found in [CFZ]_. The
    implementation is based on [CFZ]_, Theorem 1.5, Remark 1.6, and Corollary
    1.9.

    EXAMPLES::

        sage: Asso = polytopes.associahedron(['A',2]); Asso
        Generalized associahedron of type ['A', 2] with 5 vertices

        sage: sorted(Asso.Hrepresentation(), key=repr)
        [An inequality (-1, 0) x + 1 >= 0,
         An inequality (0, -1) x + 1 >= 0,
         An inequality (0, 1) x + 1 >= 0,
         An inequality (1, 0) x + 1 >= 0,
         An inequality (1, 1) x + 1 >= 0]

        sage: Asso.Vrepresentation()
        (A vertex at (1, -1), A vertex at (1, 1), A vertex at (-1, 1),
         A vertex at (-1, 0), A vertex at (0, -1))

        sage: polytopes.associahedron(['B',2])
        Generalized associahedron of type ['B', 2] with 6 vertices

    The two pictures of [CFZ]_ can be recovered with::

        sage: Asso = polytopes.associahedron(['A',3]); Asso
        Generalized associahedron of type ['A', 3] with 14 vertices
        sage: Asso.plot()  # long time
        Graphics3d Object

        sage: Asso = polytopes.associahedron(['B',3]); Asso
        Generalized associahedron of type ['B', 3] with 20 vertices
        sage: Asso.plot()  # long time
        Graphics3d Object

    TESTS::

        sage: sorted(polytopes.associahedron(['A',3]).vertices())
        [A vertex at (-3/2, 0, -1/2), A vertex at (-3/2, 0, 3/2),
         A vertex at (-3/2, 1, -3/2), A vertex at (-3/2, 2, -3/2),
         A vertex at (-3/2, 2, 3/2), A vertex at (-1/2, -1, -1/2),
         A vertex at (-1/2, 0, -3/2), A vertex at (1/2, -2, 1/2),
         A vertex at (1/2, -2, 3/2), A vertex at (3/2, -2, 1/2),
         A vertex at (3/2, -2, 3/2), A vertex at (3/2, 0, -3/2),
         A vertex at (3/2, 2, -3/2), A vertex at (3/2, 2, 3/2)]

        sage: sorted(polytopes.associahedron(['B',3]).vertices())
        [A vertex at (-3, 0, 0), A vertex at (-3, 0, 3),
         A vertex at (-3, 2, -2), A vertex at (-3, 4, -3),
         A vertex at (-3, 5, -3), A vertex at (-3, 5, 3),
         A vertex at (-2, 1, -2), A vertex at (-2, 3, -3),
         A vertex at (-1, -2, 0), A vertex at (-1, -1, -1),
         A vertex at (1, -4, 1), A vertex at (1, -3, 0),
         A vertex at (2, -5, 2), A vertex at (2, -5, 3),
         A vertex at (3, -5, 2), A vertex at (3, -5, 3),
         A vertex at (3, -3, 0), A vertex at (3, 3, -3),
         A vertex at (3, 5, -3), A vertex at (3, 5, 3)]

        sage: polytopes.associahedron(['A',4]).f_vector()
        (1, 42, 84, 56, 14, 1)
        sage: polytopes.associahedron(['B',4]).f_vector()
        (1, 70, 140, 90, 20, 1)
    """
    cartan_type = CartanType(cartan_type)
    parent = Associahedra(QQ, cartan_type.rank(), 'ppl')
    return parent(cartan_type)


class Associahedron_class(Polyhedron_QQ_ppl):
    r"""
    The Python class of an associahedron

    You should use the :func:`Associahedron` convenience function to
    construct associahedra from the Cartan type.

    TESTS::

        sage: Asso = polytopes.associahedron(['A',2]); Asso
        Generalized associahedron of type ['A', 2] with 5 vertices
        sage: TestSuite(Asso).run()
    """

    def _repr_(self):
        r"""
        Return a string representation of ``self``.

        EXAMPLES::

            sage: polytopes.associahedron(['A',3])._repr_()
            "Generalized associahedron of type ['A', 3] with 14 vertices"
        """
        msg = 'Generalized associahedron of type {} with {} vertices'
        return msg.format(self._cartan_type, self.n_vertices())

    def cartan_type(self):
        r"""
        Return the Cartan type of ``self``.

        EXAMPLES::

            sage: polytopes.associahedron(['A',3]).cartan_type()
            ['A', 3]
        """
        return self._cartan_type

    def vertices_in_root_space(self):
        r"""
        Return the vertices of ``self`` as elements in the root space.

        EXAMPLES::

            sage: Asso = polytopes.associahedron(['A',2])
            sage: Asso.vertices()
            (A vertex at (1, -1), A vertex at (1, 1),
             A vertex at (-1, 1), A vertex at (-1, 0),
             A vertex at (0, -1))

            sage: Asso.vertices_in_root_space()
            (alpha[1] - alpha[2], alpha[1] + alpha[2], -alpha[1] + alpha[2],
            -alpha[1], -alpha[2])
        """
        root_space = self._cartan_type.root_system().root_space()
        return tuple(root_space.from_vector(vector(V))
                     for V in self.vertex_generator())


class Associahedra(Polyhedra_QQ_ppl):
    """
    Parent of Associahedra of specified dimension

    EXAMPLES::

        sage: from sage.combinat.root_system.associahedron import Associahedra
        sage: parent = Associahedra(QQ,2,'ppl');  parent
        Polyhedra in QQ^2
        sage: type(parent)
        <class 'sage.combinat.root_system.associahedron.Associahedra_with_category'>
        sage: parent(['A',2])
        Generalized associahedron of type ['A', 2] with 5 vertices

    Importantly, the parent knows the dimension of the ambient
    space. If you try to construct an associahedron of a different
    dimension, a ``ValueError`` is raised::

        sage: parent(['A',3])
        Traceback (most recent call last):
        ...
        ValueError: V-representation data requires a list of length ambient_dim
    """
    Element = Associahedron_class

    def _element_constructor_(self, cartan_type, **kwds):
        """
        The element constructor.

        This method is called internally when we try to convert
        something into an element. In this case, the only thing that
        can be converted into an associahedron is the Cartan type.

        EXAMPLES::

            sage: from sage.combinat.root_system.associahedron import Associahedra
            sage: parent = Associahedra(QQ,2,'ppl')
            sage: parent(['A',2])
            Generalized associahedron of type ['A', 2] with 5 vertices
            sage: parent._element_constructor_(['A',2])
            Generalized associahedron of type ['A', 2] with 5 vertices

        TESTS::

            sage: parent(['A', 2, 1])
            Traceback (most recent call last):
            ...
            ValueError: the Cartan type must be finite
        """
        cartan_type = CartanType(cartan_type)
        if not cartan_type.is_finite():
            raise ValueError("the Cartan type must be finite")
        root_space = cartan_type.root_system().root_space()
        # TODO: generalize this as a method of root lattice realization
        rhocheck = sum(beta.associated_coroot()
                       for beta in root_space.positive_roots()) / 2
        I = root_space.index_set()
        inequalities = []
        for orbit in root_space.almost_positive_roots_decomposition():
            c = rhocheck.coefficient(orbit[0].leading_support())
            for beta in orbit:
                inequalities.append([c] + [beta.coefficient(i) for i in I])
        associahedron = super(Associahedra, self)._element_constructor_(None, [inequalities, []])
        associahedron._cartan_type = cartan_type
        return associahedron
