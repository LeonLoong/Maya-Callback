import re, zipfile, os
from contextlib import contextmanager

def get_ArchiveVersionFormat( filename ):
	dirname, basename = os.path.split( filename )
	name, extension = os.path.splitext( basename )
	
	arcForm = '{}_%s_%s{}'.format( name, extension )
	return arcForm
	
@contextmanager
def openZip( filepath, mode= 'r' ):
	z = zipfile.ZipFile( filepath, mode, zipfile.ZIP_DEFLATED )
	yield z
	z.close()
		
def zip( source, destination, arcname = None, attempt = 3 ):
	dirname, filename = os.path.split( destination )
	if not os.path.isdir( dirname ):
		os.makedirs( dirname )
	
	with openZip( destination, 'a' if os.path.isfile( destination ) else 'w' ) as z:
		z.write( source, arcname = arcname )

def getArchiveFile( filename ):
	dirname, basename = os.path.split( filename )
	name, extension = os.path.splitext( basename )
	zipname = os.path.join( dirname, 'Archive', name + '.zip' )
	
	return zipname
			
def archive( filename, stage ):
	try:
		zipname = getArchiveFile( filename )
		arcForm = get_ArchiveVersionFormat( filename )
		arcPattern = re.compile( arcForm %( '[a-zA-Z]+', '([0-9]+)' ) )
		#arcPattern = re.compile( arcForm % '([0-9]+)', re.IGNORECASE )
		index = 0

		if os.path.isfile( zipname ):
			arc = []
			with openZip( zipname, 'r' ) as z:
				for info in z.infolist():
					match = arcPattern.match( info.filename )
					if match:
						no = int( match.group( 1 ) )
						arc.append( ( no, info.filename ) )
					
				arc.sort( cmp=lambda x,y: cmp( x[ 0 ], y[ 0 ] ) )
				
			if len( arc ) > 0:
				index = arc[ -1 ][ 0 ]
				
		zip( filename, zipname, arcForm % ( '%s', '%03d' ) % ( stage, index + 1 ) )
		return zipname
	except Exception, args:
		print ('Archiving {} failed!'.format(filename))
		raise