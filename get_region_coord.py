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

import logging
import sys
from argparse import ArgumentParser

from shapely.geometry import Point, box
from shapely import wkt

import cytomine
from cytomine.models import Property, Annotation, AnnotationTerm, AnnotationCollection, JobData, Job, TermCollection, ImageInstanceCollection, ImageInstance


def run(cyto_job, parameters):
    logging.info("----- Get region coordinates v%s -----", __version__)
    logging.info("Entering run(cyto_job=%s, parameters=%s)", cyto_job, parameters)

    job = cyto_job.job
    project = cyto_job.project
    id_image = parameters.cytomine_id_image
    id_terms = parameters.cytomine_id_terms
    import_project = parameters.cytomine_import_project
    import_image = parameters.cytomine_import_image
    import_term = parameters.cytomine_import_term
    import_user = parameters.cytomine_import_user

    job.update(status=Job.RUNNING, progress=5, statusComment="Parameters gathered...")
    
    terms = TermCollection().fetch_with_filter("project", project.id)    
    images = ImageInstanceCollection().fetch_with_filter("project", project.id)
    job.update(status=Job.RUNNING, progress=10, statusComment="Terms and images gathered...")    

    # Get the list of annotations to import
    annotations_import = AnnotationCollection(
        terms=[import_term],
        image=import_image,
        project=import_project,
        user=import_user,
        showBasic=True,
        showWKT=True,
        showUser=True,
        showTerm=True,
        showImage=True,
        includeAlgo=True
    ).fetch()

    print("Total annotations to import: ",len(annotations_import))
    
    annotations = AnnotationCollection()

    # progress_delta=100-(progress)/len(annotations_import)

    for anno in annotations_import:
        roi_geometry = wkt.loads(anno.location)        
        annotations.append(Annotation(
            location=roi_geometry.wkt,
            id_image=id_image,
            id_project=project.id,
            id_terms=[id_terms]))   
    annotations.save()

        # annotation_import = Annotation(location=roi_geometry.wkt, id_image=id_image, id_project=project.id).save()
        # # print(annotation_import.id)
        # AnnotationTerm(annotation_import.id, [id_terms]).save()  
        # job.update(status=Job.RUNNING, progress=progress, statusComment="Copying region coordinates....")
            # annotation.delete()
                

if __name__ == "__main__":
    logging.debug("Command: %s", sys.argv)
    with cytomine.CytomineJob.from_cli(sys.argv) as cyto_job:
         run(cyto_job, cyto_job.parameters)
