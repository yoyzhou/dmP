'''
Created on Aug 21, 2012

@author: yoyzhou
'''


class Tree(object):
    '''
        A Python implementation of Tree data structure 
    '''
       
    def __init__(self, data = None, children = None):
        '''
        @param data: content of this node
        @param children: sub node(s) of tree, could be None, child (single) or children (multiple)
        '''
        self.data = data
        self.__children = []
        self.__parent=None  #private parent attribute
        
        if children: #construct a tree with child or __children
            if isinstance(children, Tree):
                self.__children.append(children)
                children.__parent = self 
            elif isinstance(children, list):
                for child in children:
                    if isinstance(child, Tree):
                        self.__children.append(child)
                        child.__parent = self
                    else:
                        raise TypeError('Child of Tree should be a Tree type.')      
            else:
                raise TypeError('Child of Tree should be a Tree type')
    
    
    def __setattr__(self, name, value):
        
        r"""
            Hide the __parent and __children attribute from using dot assignment.
            To add __children, please use addChild or addChildren method; And
            node's parent isn't assignable
        """
      
        if name in ('parent', '__parent', 'children'):
                raise AttributeError("To add children, please use addChild or addChildren method.")
        else:
            super().__setattr__(name, value)
            
    def getParent(self):
        """
            Get node's parent node.
        """
        return self.__parent
    
    def getChildren(self):
        """
            Get node's all child nodes.
        """
        return self.__children
    
    def getChild(self, index):
        """  
            Get node's No. index child node.
            @param index: Which child node to get in children list, starts with 0 to number of children - 1
            @return:  A Tree node presenting the number index child
            @raise IndexError: if the index is out of range 
        """
        try:
            return self.__children[index]
        except IndexError:
            raise IndexError("Index starts with 0 to number of children - 1")
    
    def getNode(self, content):
        """
                         
            Get the first matching item(including self) whose data is equal to content. 
            Method uses data == content to determine whether a node's data equals to content, note if your node's data is 
            self defined class, overriding object's __eq__ might be required.
            Implement tree travel (level first) algorithm using queue

            @param content: node's content to be searched 
            @return: Return node which contains the same data as parameter content, return None if no such node
        """
        nodesQ = [self]
        
        while True and nodesQ:
            child = nodesQ[0]
            if child.data == content:
                return child
            else:
                nodesQ.extend(child.getChildren())
                del nodesQ[0]
                

    def getRoot(self):
        """
            Get root of the current node.
        """
        if self.isRoot():
            return self
        else:
            return self.getParent().getRoot()
            
    def addChild(self, child):
        """
            Add one single child node to current node
        """
        if isinstance(child, Tree):
                self.__children.append(child)
                child.__parent = self
        else:
                raise TypeError('Child of Tree should be a Tree type')
            
    def addChildren(self, children):
        """
            Add multiple child nodes to current node
        """
        if isinstance(children, list):
                for child in children:
                    if isinstance(child, Tree):
                        self.__children.append(child)
                        child.__parent = self
                    else:
                        raise TypeError('Child of Tree should be a Tree type.')      
            
    def isRoot(self):
        """
            Determine whether node is a root node or not.
        """
        if self.__parent is None:
            return True
        else:
            return False
    
    def isBranch(self):
        """
            Determine whether node is a branch node or not.
        """
        if self.__children == []:
            return True
        else:
            return False
