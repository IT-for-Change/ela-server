import os
import csv
import traceback
import configparser
from elautil import dataclasses as dc, config as cfg, logger
# Constants


def initialize():
    
    return

def file_exists(uploadPkgId, filename):
    audio_file_path = os.path.join(cfg.PKG_UPLOAD_BASE_DIR, uploadPkgId, cfg.PKG_AUDIO_REL_DIR, filename)
    return os.path.exists(audio_file_path)

def loadActivityData(packageMetadata):
    
    uploadPkgType = packageMetadata.pkgtype

    logger.info(f'Loading activity data for {packageMetadata.schoolpkgid} of type {uploadPkgType}')

    if (uploadPkgType == dc.PackageType.ECUBE.name):
        return loadActivityDataECUBE(packageMetadata)
    elif (uploadPkgType == dc.PackageType.BYRA.name):
        logger.error('Unsupported package type BYRA. Defaulting to ECUBE')
        return loadActivityDataECUBE(packageMetadata)
    elif (uploadPkgType == dc.PackageType.SIMPLE.name):
        logger.debug('Package type SIMPLE')
        return loadActivityDataSIMPLE(packageMetadata)
    else:
        logger.error(f'Unsupported package type {uploadPkgType}. Defaulting to ECUBE')
        return loadActivityDataECUBE(packageMetadata)

def loadActivityDataECUBE(packageMetadata):
    uploadPkgId = packageMetadata.schoolpkgid
    csv_file_name = uploadPkgId + '.csv'
    csv_file_path = os.path.join(cfg.PKG_UPLOAD_BASE_DIR, uploadPkgId, cfg.PKG_CSV_REL_DIR, csv_file_name)

    activityItems = []

    try:
        with open(csv_file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                userid, username, course, assignmentid, attemptnumber, time, filename = row

                try:
                    if file_exists(uploadPkgId, filename):
                        audio_file_path = os.path.join(cfg.PKG_UPLOAD_BASE_DIR, uploadPkgId, cfg.PKG_AUDIO_REL_DIR, filename)
                        item = dc.ActivityItem()
                        item.userid = userid
                        item.username = username
                        item.lessonid = course
                        item.assignmentid = assignmentid
                        item.attemptnumber = attemptnumber
                        item.attempttime = time
                        item.submissionfile = audio_file_path
                        item.packagemetadata = packageMetadata
                        activityItems.append(item)
                    else:
                        print(f"File not found: {filename}")
                except Exception as inner_exception:
                    print(f"Error processing file {filename}: {inner_exception}")
        
        return activityItems

    except Exception as outer_exception:
        print(f"Error reading CSV file: {outer_exception}")

def loadActivityDataSIMPLE(packageMetadata):

    uploadPkgId = packageMetadata.schoolpkgid
    csv_file_name = uploadPkgId + '-SIMPLE.csv'
    csv_file_path = os.path.join(cfg.PKG_UPLOAD_BASE_DIR, uploadPkgId, cfg.PKG_CSV_REL_DIR, csv_file_name)

    activityItems = []

    logger.debug(f'Loading csv file {csv_file_path}')

    try:
        with open(csv_file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                userid, username, course, assignmentid, attemptnumber, time, filename = row
                logger.debug(f'csv file line: {row}')
                try:
                    if file_exists(uploadPkgId, filename):
                        audio_file_path = os.path.join(cfg.PKG_UPLOAD_BASE_DIR, uploadPkgId, cfg.PKG_AUDIO_REL_DIR, filename)
                        item = dc.ActivityItem()
                        item.userid = ''
                        item.username = ''
                        item.lessonid = ''
                        item.assignmentid = ''
                        item.attemptnumber = ''
                        item.attempttime = ''
                        item.submissionfile = audio_file_path
                        item.packagemetadata = packageMetadata
                        activityItems.append(item)
                    else:
                        print(f"File not found: {filename}")
                except Exception as inner_exception:
                    print(f"Error processing file {filename}: {inner_exception}")
        
        return activityItems

    except Exception as outer_exception:
        print(f"Error reading CSV file: {outer_exception}")

def loadPackageMetaData(uploadPkgId,uploadPkgType):

    if (uploadPkgType == dc.PackageType.ECUBE.name):
        return loadPackageMetaDataECUBE(uploadPkgId)
    elif (uploadPkgType == dc.PackageType.BYRA.name):
        logger.error('Unsupported package type BYRA. Defaulting to ECUBE')
        return loadPackageMetaDataECUBE(uploadPkgId)
    elif (uploadPkgType == dc.PackageType.SIMPLE.name):
        logger.debug('Package type SIMPLE')
        return loadPackageMetaDataSIMPLE(uploadPkgId)
    else:
        logger.error(f'Unsupported package type {uploadPkgType}. Defaulting to ECUBE')
        return loadPackageMetaDataECUBE(uploadPkgId)


def loadPackageMetaDataECUBE(uploadPkgId):

    packageMetadataFile = uploadPkgId + '.txt'
    packageMetadataFullFile = os.path.join(cfg.PKG_UPLOAD_BASE_DIR, uploadPkgId, cfg.PKG_META_LOG_DIR, packageMetadataFile)
    
    parser = configparser.ConfigParser()
    parser.read(packageMetadataFullFile)
    metadata = dict(parser.items('ECUBE'))
    schoolCode = ''
    dataCollectedWhen = ''
    if metadata['id'] == uploadPkgId:
        schoolCode = metadata['schoolcode']
        dataCollectedWhen = metadata['starttime']
    else:
        print('LoadPackageMetadataException')
    
    if (schoolCode == None) or (dataCollectedWhen == None):
        print('LoadPackageMetadataException')
    
    packageMetadata = dc.PackageMeta()
    packageMetadata.schoolpkgid = uploadPkgId
    packageMetadata.collectiontime = dataCollectedWhen
    packageMetadata.schoolcode = schoolCode
    packageMetadata.pkgtype = dc.PackageType.ECUBE.name

    return packageMetadata

def loadPackageMetaDataBYRA(uploadPkgId):

    packageMetadataFile = uploadPkgId + '.txt'
    packageMetadataFullFile = os.path.join(cfg.PKG_UPLOAD_BASE_DIR, uploadPkgId, cfg.PKG_META_LOG_DIR, packageMetadataFile)
    
    parser = configparser.ConfigParser()
    parser.read(packageMetadataFullFile)
    metadata = dict(parser.items('ECUBE'))
    schoolCode = ''
    dataCollectedWhen = ''
    if metadata['id'] == uploadPkgId:
        schoolCode = metadata['schoolcode']
        dataCollectedWhen = metadata['starttime']
    else:
        print('LoadPackageMetadataException')
    
    if (schoolCode == None) or (dataCollectedWhen == None):
        print('LoadPackageMetadataException')
    
    packageMetadata = dc.PackageMeta()
    packageMetadata.schoolpkgid = uploadPkgId
    packageMetadata.collectiontime = dataCollectedWhen
    packageMetadata.schoolcode = schoolCode
    packageMetadata.pkgtype = dc.PackageType.BYRA.name

    return packageMetadata

def loadPackageMetaDataSIMPLE(uploadPkgId):

    packageMetadataFile = uploadPkgId + '.txt'
    packageMetadataFullFile = os.path.join(cfg.PKG_UPLOAD_BASE_DIR, uploadPkgId, cfg.PKG_META_LOG_DIR, packageMetadataFile)
    
    parser = configparser.ConfigParser()
    parser.read(packageMetadataFullFile)
    metadata = dict(parser.items('ECUBE'))
    schoolCode = ''
    dataCollectedWhen = ''
    if metadata['id'] == uploadPkgId:
        schoolCode = metadata['schoolcode']
        dataCollectedWhen = metadata['starttime']
    else:
        print('LoadPackageMetadataException')
    
    if (schoolCode == None) or (dataCollectedWhen == None):
        print('LoadPackageMetadataException')
    
    packageMetadata = dc.PackageMeta()
    packageMetadata.schoolpkgid = uploadPkgId
    packageMetadata.collectiontime = dataCollectedWhen
    packageMetadata.schoolcode = schoolCode
    packageMetadata.pkgtype = dc.PackageType.SIMPLE.name

    return packageMetadata


if __name__ == "__main__":
    try:
        packageMetadata = loadPackageMetaData('d7f1b654-4c7e-49dd-b5f9-173f447bd497')
        items = loadActivityData(packageMetadata)
        print(items)
    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
