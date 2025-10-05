package controladores;
import modelo.Persona;
import java.util.ArrayList;
import javax.swing.table.DefaultTableModel;


public class ControladorPersona {
  
    private ArrayList<Persona> personas;
    private DefaultTableModel tabla;

    public ControladorPersona(){
        this.personas = new ArrayList<>();
    }           
    
    public boolean guardarPersona(Persona persona){
        if (persona.getEdad() >= 18){
            Persona temp = buscarPersona(persona.getId());
            if (temp == null){
                if (personas.size() < 8){
                    personas.add(persona);
                    return true;                    
                }
                return false;
            }
            return false;            
        }
        return false;
    }
    
    public Persona buscarPersona(int id){
        for (int i = 0; i < personas.size(); i++){
            if (personas.get(i).getId() == id){
                return personas.get(i);            
            }
        }                  
        return null;
    }    
    
    public boolean editarPersona(Persona persona){
        Persona temp = buscarPersona(persona.getId());
        if (temp != null){
            temp.setEdad(persona.getEdad());
            temp.setNombre(persona.getNombre());
            return true;
        }
        return false;        
    }
   
    public boolean eliminarPersona(int id){
        Persona temp = buscarPersona(id);
        if (temp != null){
            return personas.remove(temp);
        }
        return false;        
    }
    
    
    public DefaultTableModel actualizarTabla(){
        String[] columnas = {"Id", "Nombre", "Edad"};
        DefaultTableModel tabla = new DefaultTableModel(columnas, 0);
       
       for (int i = 0; i < personas.size(); i++){
           Persona persona = personas.get(i);
           Object fila[] = {
               persona.getId(),
               persona.getNombre(),
               persona.getEdad()              
           };
           tabla.addRow(fila);
       }
       return tabla;
       
    }
}