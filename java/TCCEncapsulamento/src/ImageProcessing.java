
import java.awt.Image;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.apache.xmlrpc.XmlRpcException;

public class ImageProcessing {
    
    private ClientRPC client;

    public ImageProcessing() {
        client = new ClientRPC();
    }
    
    public void generateMask() {
        Object[] params = new Object[]{};
        try {
            client.getClient().execute("generate_mask", params);

        } catch (XmlRpcException e11) {
            e11.printStackTrace();
        }
    }
    
    public Image useMask(Image image) {
        Object[] params = new Object[]{Utils.getImageToByte(image)};
        Image pan = null;
        byte[] encoded = null;
        try {
            encoded = (byte[])  client.getClient().execute("use_mask_image", params);
            System.out.println(encoded.length);

        } catch (XmlRpcException e11) {
            e11.printStackTrace();
        }

        pan = Utils.getByteToImage(encoded);
        return pan;
    }
    
    public Image getPanoramicImage(Image image) {
        Object[] params = new Object[]{Utils.getImageToByte(image)};
        Image pan = null;
        byte[] encoded = null;

        try {
            encoded = (byte[])  client.getClient().execute("generate_panoramic_image", params);
        } catch (XmlRpcException e11) {
            e11.printStackTrace();
        }
        pan = Utils.getByteToImage(encoded);
        return pan;
    }

    public Image getImageWithBoxes(Image image) {
        Object[] params = new Object[]{Utils.getImageToByte(image)};
        Image pan = null;
        byte[] encoded = null;
        try {
            encoded = (byte[])  client.getClient().execute("get_image_with_boxes", params);
        } catch (XmlRpcException e11) {
            e11.printStackTrace();
        }
        pan = Utils.getByteToImage(encoded);
        return pan;
    }
    
    public Image birdsEyeView(Image image){
         try {
            return Retification.retify(image);
        } catch (Exception ex) {
            Logger.getLogger(ServerImage.class.getName()).log(Level.SEVERE, null, ex);
        }
        return null;
    }
    
    public DetectedObjectsList getObjectsDetected(Image image) {
        Object[] params = new Object[]{Utils.getImageToByte(image)};
        String res;
        byte[] encoded = null;
        try {
            encoded = (byte[]) client.getClient().execute("get_objects_list_by_image", params);

        } catch (XmlRpcException e11) {
            e11.printStackTrace();
        }
        res = new String(encoded);
        DetectedObjectsList list = new DetectedObjectsList();
        String[] points = res.split("\n");
        for (String i : points) {
            String[] positions = i.split(";");
            DetectedObject de = new DetectedObject(Integer.parseInt(positions[0]), Integer.parseInt(positions[1]), Integer.parseInt(positions[2]), Integer.parseInt(positions[3]));
            list.add(de);
        }
        
        return list;
    }
}
