from PyQt5.QtGui import QStandardItem


class RequirementNode(QStandardItem):

    def __init__(
        self, 
        module: type,
        reference: str, 
        heading: str, 
        level: int,
        outlinks: list[str],
        inlinks: list[str],        
        file_references: list[str],
        columns_data: list[str],
        is_covered = None,        
        ):

        super().__init__()
        self.setEditable(False)

        self.MODULE = module
        self.reference = reference
        self.heading = heading
        self.level = level

        
        if outlinks:
            self.outlinks = [o.strip() for o in outlinks]
        else:
            self.outlinks = []
        if inlinks:
            self.inlinks = [i.strip() for i in inlinks]
        else:
            self.inlinks = []

        self.columns_data = columns_data  # list

        if self.heading:
            self.setText(heading)
        else:
            self.setText(reference)  

        self.node_icon = None      



    @property
    def is_covered(self):
        is_covered = self.MODULE._coverage_dict.get(self.reference.lower(), "Not Calculated")
        if is_covered == "Not Calculated":
            return None
        elif is_covered:
            return True
        else:
            return False

    

    def update_icon(self):        
        if self.is_covered == None and self.reference.lower() in self.MODULE.ignore_list:
            self.setIcon(self.MODULE.ICON_IGNORED)
            self.node_icon = None
        
        elif self.is_covered == None:
            self.setIcon(self.MODULE.ICON_NONE)
            self.node_icon = None
        

        elif self.is_covered:
            self.setIcon(self.MODULE.ICON_COVERED)
            self.node_icon = "green"
        else:
            self.setIcon(self.MODULE.ICON_NOT_COVERED)
            self.node_icon = "red"
        self.update_parents_icons()




    def update_parents_icons(self):
        while isinstance(self, RequirementNode):
            parent = self.parent()
            children = []
            green = False
            red = False
            for row in range(parent.rowCount()):
                children.append(parent.child(row))

            for child in children:
                if child.node_icon == "red":
                    red = True
                elif child.node_icon == "green":
                    green = True

            if red:
                self.parent().setIcon(self.MODULE.ICON_NOT_COVERED)
                self.parent().node_icon = "red"
            elif green:
                self.parent().setIcon(self.MODULE.ICON_COVERED)
                self.parent().node_icon = "green"
            else:
                self.parent().setIcon(self.MODULE.ICON_NONE) if isinstance(self.parent(), RequirementNode) else self.parent().setIcon(self.MODULE.ICON_DOORS)
                self.parent().node_icon = None

            self = self.parent()            

        



    @property
    def file_references(self):
        file_references = self.MODULE._coverage_dict.get(self.reference.lower(), [])
        return file_references          



    def add_to_ignore_list(self):
        if not self.hasChildren():  # if it is not Heading
            # self.update_coverage(None)
            self.MODULE._coverage_dict.pop(self.reference.lower())
            # self.MODULE.ignore_list.add(self.reference.lower())
            self.MODULE.ignore_list.append(self.reference.lower())
            self.update_icon()
            self.MODULE.update_title_text()

    def remove_from_ignore_list(self, remove_note=False):
        if not self.hasChildren():  # if it is not Heading
            if self.reference.lower() in self.MODULE.ignore_list or self.reference in self.MODULE.ignore_list:            
                # self.update_coverage(False)
                try:
                    self.MODULE.ignore_list.remove(self.reference)
                except ValueError:
                    self.MODULE.ignore_list.remove(self.reference.lower())

                self.MODULE._coverage_dict.update({self.reference.lower() : []})
                if remove_note:
                    self.MODULE.notes.pop(self.reference.lower(), None)
                self.update_icon()
                self.MODULE.update_title_text()



    @property
    def note(self) -> str:
        return self.MODULE.notes.get(self.reference.lower(), "")

    @note.setter
    def note(self, text: str) -> None:
        if text.strip() != "":
            self.MODULE.notes.update({self.reference.lower(): text})
        else:     
            self.MODULE.notes.pop(self.reference.lower(), None)

