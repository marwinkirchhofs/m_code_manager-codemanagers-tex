#!/usr/bin/env python3

# TODO: think about making chapter_order some sort of standard file type, 
# probably yaml (or json if that's necessary for some reason, but yaml should be 
# fine, no outdated tcl versions involved here) -> another benefit that would 
# have: You can include ordering for the subsections, and the pyhton parsing 
# becomes a little more standardized

import os
from operator import itemgetter

import code_manager
import m_code_manager.util.files as files

LANG_IDENTIFIERS = ["latex"]


class TexCodeManager(code_manager.CodeManager):

    PLACEHOLDERS = {
            'DIR_SRC':                      "src",
            'DIR_UTIL':                     "util",
            'FILE_TEX_MAIN_BASE':           "main",
            'FILE_CHAPTER_ORDER':           "chapter_order",
            'FILE_CHAPTERS':                "chapters.tex",
            'FILE_TEX_PACKAGES':            "packages.tex",
            'FILE_TEX_COMMANDS':            "commands.tex",
            'FILE_TEX_COLORS':              "colors.tex",
            'SCRIPT_INCLUDE_CHAPTERS':      "include_chapters.py",
            'EXAMPLE_CHAPTER':              "example",
    }

    def __init__(self):
        # why passing the language to the base class init? See (way too 
        # extensive) comment in python_code_manager
        super().__init__("tex")

    def _command_project(self, project="", name="document", 
                         tex_engine="pdflatex", **kwargs):
        '''
        :project: name for the created project
        :name: currently unused, see tex_engine
        :tex_engine: currently unused, after an update is supposed as the entry 
        to a field in a project config
        '''
        # TODO: git option

        ##############################
        # PROJECT DIRECTORIES
        ##############################

        if project:
            files.create_dir(project)
            os.chdir(project)

        project_dirs = itemgetter(
                'DIR_SRC', 'DIR_UTIL',
                )(self.PLACEHOLDERS)
        for directory in project_dirs:
            files.create_dir(directory)

        ##############################
        # TEMPLATES
        ##############################

        # MAIN
        s_target_file = self.PLACEHOLDERS["FILE_TEX_MAIN_BASE"] + ".tex"
        if self._check_target_edit_allowed(s_target_file):
            template_out = self._load_template("main")
            self._write_template(template_out, s_target_file)

        # UTIL/COMMANDS
        s_target_file = os.path.join(
                self.PLACEHOLDERS["DIR_UTIL"],
                self.PLACEHOLDERS["FILE_TEX_COMMANDS"])
        if self._check_target_edit_allowed(s_target_file):
            template_out = self._load_template("commands")
            self._write_template(template_out, s_target_file)

        # UTIL/ACRONYMS
        # TODO

        # UTIL/PACKAGES
        s_target_file = os.path.join(
                self.PLACEHOLDERS["DIR_UTIL"],
                self.PLACEHOLDERS["FILE_TEX_PACKAGES"])
        if self._check_target_edit_allowed(s_target_file):
            template_out = self._load_template("packages")
            self._write_template(template_out, s_target_file)

        # UTIL/COLORS
        s_target_file = os.path.join(
                self.PLACEHOLDERS["DIR_UTIL"],
                self.PLACEHOLDERS["FILE_TEX_COLORS"])
        if self._check_target_edit_allowed(s_target_file):
            template_out = self._load_template("colors")
            self._write_template(template_out, s_target_file)

        # EXAMPLE CHAPTERS
        s_target_file = self.PLACEHOLDERS["FILE_CHAPTER_ORDER"]
        if self._check_target_edit_allowed(s_target_file):
            template_out = self._load_template("chapter_order")
            self._write_template(template_out, s_target_file)

        # EXAMPLE CHAPTER
        s_dir_example_chapter = os.path.join(
                self.PLACEHOLDERS["DIR_SRC"], self.PLACEHOLDERS["EXAMPLE_CHAPTER"])
        files.create_dir(s_dir_example_chapter)

        s_target_file = os.path.join(s_dir_example_chapter,
                                     self.PLACEHOLDERS["EXAMPLE_CHAPTER"] + "_section.tex")
        if self._check_target_edit_allowed(s_target_file):
            template_out = self._load_template("example_section", dict_placeholders={
                        "EXAMPLE_CHAPTER_TITLE": self.PLACEHOLDERS["EXAMPLE_CHAPTER"].capitalize()
                        })
            self._write_template(template_out, s_target_file)
