
import java.awt.Graphics;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import sun.misc.BASE64Decoder;


public class Utils {

    public static byte[] getImageToByte(Image image) {
        BufferedImage bi = new BufferedImage(image.getWidth(null), image.getHeight(null), BufferedImage.TYPE_INT_RGB);
        Graphics bg = bi.getGraphics();
        bg.drawImage(image, 0, 0, null);
        bg.dispose();

        ByteArrayOutputStream buff = new ByteArrayOutputStream();
        try {
            ImageIO.write(bi, "png", buff);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return buff.toByteArray();
    }

    public static BufferedImage decodeToImage(String imageString) {
        BufferedImage image = null;
        byte[] imageByte;
        try {
            BASE64Decoder decoder = new BASE64Decoder();
            imageByte = decoder.decodeBuffer(imageString);
            ByteArrayInputStream bis = new ByteArrayInputStream(imageByte);
            image = ImageIO.read(bis);
            bis.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return image;
    }

    public static Image getByteToImage(byte[] bytes) {

        return new ImageIcon(bytes).getImage();

    }

    public static Image getScaledDimension(Image image, int bound_height, int bound_width) {

        int original_width = image.getWidth(null);
        int original_height = image.getHeight(null);

        int new_width = original_width;
        int new_height = original_height;

        if (original_width > bound_width) {
            new_width = bound_width;
            new_height = (new_width * original_height) / original_width;
        }
        if (new_height > bound_height) {
            new_height = bound_height;
            new_width = (new_height * original_width) / original_height;
        }
        return image.getScaledInstance(new_width, new_height, Image.SCALE_SMOOTH);
    }
   

    
}
