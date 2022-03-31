from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from image_processing_by_id import ProcessingById
from image_processing_by_image import ProcessingByImage
from support_functions import Support


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
class Server:
    
    processing_by_image = ProcessingByImage()
    processing_by_id = ProcessingById()
    support = Support()
    
    def serve(self):
        print('starting server...')
        with SimpleXMLRPCServer(('localhost', 8065), requestHandler=RequestHandler) as server:
            server.register_introspection_functions()

            server.register_function(pow)

            @server.register_function(name='generate_panoramic_image')
            def generate_panoramic_image(image):
                return self.processing_by_image.generate_panoramic(image.data)

            @server.register_function(name='generate_birds_eye_by_image')
            def generate_birds_eye_by_image(image, dist_params, angle_params, center_col, center_line):
                return self.processing_by_image.generate_birds_eye(image.data, dist_params, angle_params, center_col, center_line)

            @server.register_function(name='get_objects_list_by_image')
            def get_objects_list_by_image(image):
                return self.processing_by_image.get_objects_list(image.data)

            @server.register_function(name='get_image_with_boxes')
            def get_image_with_boxes(image):
                return self.processing_by_image.get_image_with_boxes(image.data)

            @server.register_function(name='use_mask_image')
            def use_mask_image(image):
                return self.processing_by_image.use_mask(image.data)

            @server.register_function(name='generate_birds_eye_by_id')
            def generate_birds_eye_by_id(image,  dist_params, angle_params, center_col, center_line):
                print(image, dist_params, angle_params,  center_col, center_line)
                return self.processing_by_id.generate_birds_eye(image, dist_params, angle_params, center_col, center_line)

            @server.register_function(name='save_image_get_id')
            def save_image_get_id(image):
                return self.processing_by_id.save_image_get_id(image.data)

            @server.register_function(name='generate_panoramic_by_id')
            def generate_panoramic_by_id(id):
                return self.processing_by_id.generate_panoramic(id)
            
            @server.register_function(name='get_image_with_boxes_by_id')
            def get_image_with_boxes_by_id(id):
                return self.processing_by_id.get_image_with_boxes(id)

            @server.register_function(name='get_objects_list_by_id')
            def get_objects_list_by_id(id):
                return self.processing_by_id.get_objects_list(id)
            
            @server.register_function(name='use_mask_by_id')
            def use_mask_by_id(id):
                return self.processing_by_id.use_mask(id)
            
            @server.register_function(name='generate_mask')
            def generate_mask():
                return self.support.generate_mask()

            @server.register_function(name='calibrate')
            def calibrate(centroCol, centroLin):
                return self.support.calibrate(centroCol, centroLin)

            print('done')
            server.serve_forever()     

if __name__ == '__main__':
    server = Server()
    server.serve()

