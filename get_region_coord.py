# -*- coding: utf-8 -*-

# * Copyright (c) 2009-2018. Authors: see NOTICE file.
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *      http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.

__author__ = "WSH Munirah W Ahmad 5 Jan 2022 <wshmunirah@gmail.com>"
__copyright__ = "Apache 2 license. Made by Multimedia University Cytomine Team, Cyberjaya, Malaysia, http://cytomine.mmu.edu.my/"
__version__ = "1.0.0"

import os
import logging
import sys
from argparse import ArgumentParser

from shapely.geometry import Point, box
from shapely import wkt

import cytomine
from cytomine import Cytomine, CytomineJob
from cytomine.models import Property, Annotation, AnnotationTerm, AnnotationCollection, JobData, Job, User, TermCollection, ImageInstanceCollection, ImageInstance


# def run(cyto_job, parameters):
#     logging.info("----- Get region coordinates v%s -----", __version__)
#     logging.info("Entering run(cyto_job=%s, parameters=%s)", cyto_job, parameters)

#     job = cyto_job.job
#     user = job.userJob
#     project = cyto_job.project
#     id_image = parameters.cytomine_id_image
#     id_term = parameters.cytomine_id_term
#     import_project = parameters.cytomine_import_project
#     import_image = parameters.cytomine_import_image
#     import_term = parameters.cytomine_import_term
#     import_user = parameters.cytomine_import_user

#     job.update(status=Job.RUNNING, progress=10, statusComment="Parameters gathered...")
    
#     # Get the list of annotations to import
#     annotations_import = AnnotationCollection(
#         terms=[import_term],
#         image=import_image,
#         project=import_project,
#         showBasic=True,
#         showWKT=True,
#         showUser=True,
#         showTerm=True,
#         showImage=True,
#         includeAlgo=True
#     ).fetch()

#     print("Total annotations to import: ",len(annotations_import))    

#     job.update(status=Job.RUNNING, progress=20, statusComment="Gathered annotations to import...")
    
#     for anno in annotations_import:
#         roi_geometry = wkt.loads(anno.location)        
#         Annotation(
#             location=roi_geometry.wkt,
#             user=user,
#             id_image=id_image,
#             id_project=project.id,
#             id_terms=[id_term]).save()
                

# if __name__ == "__main__":
#     logging.debug("Command: %s", sys.argv)
#     with cytomine.CytomineJob.from_cli(sys.argv) as cyto_job:
#          run(cyto_job, cyto_job.parameters)

def main(argv):
    with CytomineJob.from_cli(argv) as conn:
    # with Cytomine(argv) as conn:
        print(conn.parameters)

        conn.job.update(status=Job.RUNNING, progress=0, statusComment="Initialization...")
        base_path = "{}".format(os.getenv("HOME")) # Mandatory for Singularity
        working_path = os.path.join(base_path,str(conn.job.id))
        current_dir = os.path.dirname(__file__)

        id_project = conn.parameters.cytomine_id_project
        id_image = conn.parameters.cytomine_id_image
        id_term = conn.parameters.cytomine_id_term
        import_project = conn.parameters.cytomine_import_project
        import_image = conn.parameters.cytomine_import_image
        import_term = conn.parameters.cytomine_import_term
        import_user = conn.parameters.cytomine_import_user
        
        terms = TermCollection().fetch_with_filter("project", conn.parameters.cytomine_id_project)
        conn.job.update(status=Job.RUNNING, progress=10, statusComment="Terms collected...")
        print(terms)

        # Get the list of annotations to import
        annotations_import = AnnotationCollection(
            terms=[import_term],
            image=import_image,
            project=import_project,
            showBasic=True,
            showWKT=True,
            showUser=True,
            showTerm=True,
            showImage=True,
            includeAlgo=True
        ).fetch()
    
        print("Total annotations to import: ",len(annotations_import))    
    
        # job.update(status=Job.RUNNING, progress=20, statusComment="Gathered annotations to import...")
        
        for anno in annotations_import:
            roi_geometry = wkt.loads(anno.location)        
            Annotation(
                location=roi_geometry.wkt,
                # user=user,
                id_image=id_image,
                id_project=id_project,
                id_terms=[id_term]).save()
               

if __name__ == "__main__":
    main(sys.argv[1:])
