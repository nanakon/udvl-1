import tableau

class TableauBuilder(object):
    def build(self, signedFormulas):
        """ Vytvori a vrati uzavrete alebo uplne tablo pre zoznam oznacenych formul. """

        # aby sa vrcholy cislovali od 1
        tableau.Node.resetLastNumber()

        # vyplnime prve vrcholy podla zoznamu vstupnych formul
        fakeRoot = tableau.Node(False, None)
        node = fakeRoot
        alphas = []
        betas = []
        closed = False
        for sf in signedFormulas:
            node = self.addNewFormula(node, sf, alphas, betas, [])
            if node.closed:
                closed = True
        tabl = fakeRoot.children[0]
        if closed:
            node.closed = True
            return tabl

        self.expand(node, alphas, betas, [])
        return tabl

    def addNewFormula(self, node, sf, alphas, betas, branchFormulas):
        sign, formula = sf
        #vytvorime novy vrchol
        newNode = tableau.Node(sign, formula)
        node.children.append(newNode)   #pridame pod aktualny
        #node = newNode                  #posunieme sa nan
        #self.addNewFormula(newNode, sf, alphas, betas) #pridame do alpha/beta, skontrolujeme uzavretost...
        if formula.getType(sign) == tableau.ALPHA:
            alphas.append(newNode)
        elif formula.getType(sign) == tableau.BETA:
            betas.append(newNode)
            branchFormulas.append(newNode)
        else:
            pass
     
        return newNode        

    def expand(self, node, alphas, betas, branchFormulas):
        while alphas:
            alpha = alphas.pop()
            for sf in alpha.formula.signedSubf(alpha.sign):
               node = self.addNewFormula(node, sf, alphas, betas, branchFormulas)
               node.source = alpha
               if node.closed:
                    return #ak sme uzavreli, nema zmysel ist dalej
        #minuli sa alphas, rozbijeme nejaku betu
        if betas:
            beta = betas.pop()
            for sf in beta.formula.signedSubf(beta.sign):
                newAlphas = []
                newBetas = betas[:] #skopiruje betas
                newNode = self.addNewFormula(node, sf, newAlphas, newBetas, branchFormulas)
                newNode.source = beta
                self.expand(newNode, newAlphas, newBetas, branchFormulas)
                
                                

# vim: set sw=4 ts=8 sts=4 et :
