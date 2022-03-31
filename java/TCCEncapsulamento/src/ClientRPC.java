
import java.net.URL;
import java.net.MalformedURLException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;

public class ClientRPC {

    private String host = "localhost";
    private String port = "8065";
    private XmlRpcClient client;

    public ClientRPC() {
        XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
        try {
            config.setServerURL(new URL("http://" + host + ":" + port + "/RPC2"));
        } catch (MalformedURLException ex) {
            System.err.println("Servidor não encontrado");
        }
        client = new XmlRpcClient();
        client.setConfig(config);
    }

    public void setHost(String host) {
        this.host = host;
    }

    public void setPort(String port) {
        this.port = port;
    }

    public XmlRpcClient getClient() {
        return client;
    }

    public void setClient(XmlRpcClient client) {
        this.client = client;
    }

    

}
