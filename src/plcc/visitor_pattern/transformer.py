# Code in this file is a heavily modified version of Marc Brinkmann's visitor
# module. His original copyright and license information is below. ourPLCC
# maintains the copyright on changes made to this module, and licenses it
# under GPL v3.0 or higher.


# Copyright (c) 2015 Marc Brinkmann

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

class Transformer(object):
    def visit(self, node, **kws):
        '''
        Dispatches to a visit method based on the type of node and returns
        its result. If no such method exists, returns node.

        **kws is passed to the dispatched method. If used with a Transformation,
        kws contains the results of visiting child attributes of node.
        '''
        if isinstance(node, type):
            mro = node.mro()
        else:
            mro = type(node).mro()
        for cls in mro:
            meth = getattr(self, 'visit_' + cls.__name__, None)
            if meth is not None:
                return meth(node, **kws)
            else:
                return node
