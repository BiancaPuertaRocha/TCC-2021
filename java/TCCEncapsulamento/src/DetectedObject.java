
import java.awt.Point;
import java.awt.Rectangle;


public class DetectedObject {
    private final int x;
    private final int y;
    private final int height;
    private final int width;

    public DetectedObject(int x, int y, int height, int width) {
        this.x = x;
        this.y = y;
        this.height = height;
        this.width = width;
      
    }
    
    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public int getHeight() {
        return height;
    }

    public int getWidth() {
        return width;
    }
    
    public Rectangle getBox(){
        Rectangle boundingBox = new Rectangle(x, y, width, height);
        return boundingBox;
    }

    public Point getTopL() {
        Point topL = new Point(x, y);
        return topL;
    }

    public Point getBotR() {
        Point botR = new Point(x+width, y+height);
        return botR;
    }
    
   
    @Override
    public String toString() {
        return "DetectedObject{" + "x=" + x + ", y=" + y + ", height=" + height + ", width=" + width + '}';
    }

    
}
