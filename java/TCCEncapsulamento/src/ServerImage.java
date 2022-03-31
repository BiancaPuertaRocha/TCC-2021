
import java.awt.Image;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.apache.xmlrpc.XmlRpcException;

public class ServerImage {

    private String id;
    private ClientRPC cliente;

    public ServerImage(Image image) {
        cliente = new ClientRPC();
        Object[] params = new Object[]{Utils.getImageToByte(image)};
        String id = null;
        try {
            id = (String) cliente.getClient().execute("save_image_get_id", params);

        } catch (XmlRpcException e11) {
            e11.printStackTrace();
        }
        if (id.length() > 0) {

            this.id = id;
        } else {
            System.err.println("Fail to receive id image from server");
        }
    }

    public String getId() {
        return id;

    }

    public Image getPanoramicImage() {
        Object[] params = new Object[]{this.id};
        Image pan = null;
        byte[] encoded = null;
        try {
            encoded = (byte[]) cliente.getClient().execute("generate_panoramic_by_id", params);

        } catch (XmlRpcException e11) {
            e11.printStackTrace();
        }
        pan = Utils.getByteToImage(encoded);
        return pan;
    }

    public Image getBirdsEyeView() {

        try {
            return Retification.retify(id);
        } catch (Exception ex) {
            Logger.getLogger(ServerImage.class.getName()).log(Level.SEVERE, null, ex);
        }
        return null;
    }

    public DetectedObjectsList getObjectsDetected() {
        Object[] params = new Object[]{this.id};
        String res;
        byte[] encoded = null;
        try {
            encoded = (byte[]) cliente.getClient().execute("get_objects_list_by_id", params);

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

    public Image getImageWithBoxes() {
        Object[] params = new Object[]{this.id};
        Image pan = null;
        byte[] encoded = null;
        try {
            encoded = (byte[]) cliente.getClient().execute("get_image_with_boxes_by_id", params);
            System.out.println(encoded.length);

        } catch (XmlRpcException e11) {
            e11.printStackTrace();
        }
        pan = Utils.getByteToImage(encoded);
        return pan;
    }

    public void generateMask() {
        Object[] params = new Object[]{};
        try {
            cliente.getClient().execute("generate_mask", params);

        } catch (XmlRpcException e11) {
            e11.printStackTrace();
        }
    }

    public Image useMask() {
        Object[] params = new Object[]{this.id};
        Image pan = null;
        byte[] encoded = null;
        try {
            encoded = (byte[]) cliente.getClient().execute("use_mask_by_id", params);
        } catch (XmlRpcException e11) {
            e11.printStackTrace();
        }
        pan = Utils.getByteToImage(encoded);
        return pan;
    }
}
