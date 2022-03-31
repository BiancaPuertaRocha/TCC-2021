
import java.awt.Image;
import java.util.ArrayList;
import org.apache.xmlrpc.XmlRpcException;

public abstract class Retification {

    private static ArrayList<Double> parametersAngle = new ArrayList<>();
    private static ArrayList<Double> parametersRadius = new ArrayList<>();
    private static ClientRPC client = new ClientRPC();
    private static int centerLine;
    private static int centerCol;

    public static void generateParams( int centerCol,int centerLine) {
        Retification.centerLine = centerLine;
        Retification.centerCol = centerCol;
        Object[] params = new Object[]{ centerCol, centerLine};
        byte[] encoded = null;
        try {
            encoded = (byte[]) client.getClient().execute("calibrate", params);

        } catch (XmlRpcException e11) {
            e11.printStackTrace();
        }
        String res = new String(encoded);
        String[] parameters = res.split("\n");
        String[] angle = parameters[1].split(";");
        String[] rad = parameters[0].split(";");
        for (String r : rad) {
            Retification.parametersRadius.add(Double.parseDouble(r));
        }
        for (String a : angle) {
            Retification.parametersAngle.add(Double.parseDouble(a));
        }
        System.out.println(res);

    }

    public static Image retify(Image image) throws Exception {
        if (parametersAngle.size() > 0 && parametersRadius.size() > 0) {
            Object[] params = new Object[]{Utils.getImageToByte(image),  parametersRadius,parametersAngle, centerCol, centerLine};
            Image pan = null;
            byte[] encoded = null;
            try {
                encoded = (byte[]) client.getClient().execute("generate_birds_eye_by_image", params);
                System.out.println(encoded.length);

            } catch (XmlRpcException e11) {
                e11.printStackTrace();
            }

            pan = Utils.getByteToImage(encoded);
            return pan;
        }
        throw new Exception("Parameters not found");
    }

    public static Image retify(String imageCode) throws Exception {
        if (parametersAngle.size() > 0 && parametersRadius.size() > 0) {
            Object[] params = new Object[]{imageCode, parametersRadius, parametersAngle, centerCol, centerLine};
            Image pan = null;
            byte[] encoded = null;
            try {
                encoded = (byte[]) client.getClient().execute("generate_birds_eye_by_id", params);
                System.out.println(encoded.length);

            } catch (XmlRpcException e11) {
                e11.printStackTrace();
            }

            pan = Utils.getByteToImage(encoded);
            return pan;
        } else {

        }

        throw new Exception("Parameters not found");
    }

    public static ArrayList<Double> getParametersAngle() {
        return parametersAngle;
    }

    public static ArrayList<Double> getParametersRadius() {
        return parametersRadius;
    }

}
