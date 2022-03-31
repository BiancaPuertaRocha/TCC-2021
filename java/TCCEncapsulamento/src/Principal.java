
import java.awt.Image;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.filechooser.FileNameExtensionFilter;

public class Principal extends JFrame {

    public static void main(String[] args) {
        File file;
        Image image = null;
        JFileChooser jfc = new JFileChooser();
        jfc.setDialogTitle("Selecione a imagem de perfil");
        jfc.setFileSelectionMode(JFileChooser.FILES_ONLY);

        FileNameExtensionFilter ext = new FileNameExtensionFilter("Imagem", "png", "jpg", "bmp");

        jfc.setFileFilter(ext);

        int r = jfc.showOpenDialog(null);

        if (r == JFileChooser.APPROVE_OPTION) {
            file = jfc.getSelectedFile();
            image = null;
            try {
                image = ImageIO.read(file);

            } catch (IOException ex) {
                JOptionPane.showMessageDialog(null, "Impossível carregar imagem!");
            } finally {

                ServerImage si = new ServerImage(image);
                System.out.println("id ---- " + si.getId());
                
                si.getPanoramicImage();

            }
        }

    }
}
