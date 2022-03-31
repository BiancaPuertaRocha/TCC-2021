
import java.awt.Point;
import java.awt.Rectangle;
import java.util.ArrayList;

public class DetectedObjectsList {

    private ArrayList<DetectedObject> list = new ArrayList();

    public void add(DetectedObject e) {
        list.add(e);
    }

    public DetectedObject get(int i) {
        return list.get(i);
    }

    public void removeItem(DetectedObject e) {
        list.remove(e);
    }

    public void remove(int i) {
        list.remove(i);
    }

    public ArrayList<Rectangle> getRectangleList() {
        ArrayList<Rectangle> recList = new ArrayList<>();
        for (DetectedObject i : this.list) {
            recList.add(i.getBox());
        }
        return recList;
    }

    public ArrayList<Point> getPoints() {
        ArrayList<Point> points = new ArrayList<>();
        for (DetectedObject i : this.list) {
            points.add(i.getTopL());
            points.add(i.getBotR());
        }
        return points;
    }

    public ArrayList<Point> getPointsTopL() {
        ArrayList<Point> points = new ArrayList<>();
        for (DetectedObject i : this.list) {
            points.add(i.getTopL());
        }
        return points;
    }

    public ArrayList<Point> getPointsBotR() {
        ArrayList<Point> points = new ArrayList<>();
        for (DetectedObject i : this.list) {
            points.add(i.getBotR());
        }
        return points;
    }

    public ArrayList<DetectedObject> getList() {
        return list;
    }
    
}
