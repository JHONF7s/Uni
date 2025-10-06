
package controladores;
import modelo.Estudiante;
import java.util.ArrayList;
import javax.swing.table.DefaultTableModel;

public class ControladorEstudiante {
    private ArrayList<Estudiante> estudiantes;
    
    
    public ControladorEstudiante(){
        this.estudiantes = new ArrayList<>();
    }
    
    public boolean guardarEstudiante(Estudiante estudiante){
        Estudiante estutmp = buscarEstudiante(estudiante.getId());
        if (estutmp == null){
            estudiantes.add(estudiante);
            return true;
        }
        return false;
        
    }
    
     public Estudiante buscarEstudiante(int id){
       
        for (int i = 0; i < estudiantes.size(); i++){
            if (estudiantes.get(i).getId() == id){
                return estudiantes.get(i);
            }
        }
        return null;        
    }
    
    public Estudiante buscarEstudiante(String id){
        if (!id.isEmpty()){
            for (int i = 0; i < estudiantes.size(); i++){
                if (estudiantes.get(i).getId() == Integer.parseInt(id)){
                    return estudiantes.get(i);
                }
            }
            return null;
        }
        return null;
    }
    
    public boolean actualizarEstudiante(Estudiante estudianteNuevo){
        Estudiante estudiante = buscarEstudiante(estudianteNuevo.getId());
        if (estudiante != null){
            estudiante.setNombre(estudianteNuevo.getNombre());
            estudiante.setEdad(estudianteNuevo.getEdad());
            estudiante.setNotas(estudianteNuevo.getNotas());
            return true;
        }
        return false;        
    }
    
    public boolean eliminarEstudiante(String id){
        Estudiante estudiante = buscarEstudiante(id);
        if (estudiante != null){
            estudiantes.remove(estudiante);
            return true;
        }
        return false;
    }
    
    
//    public DefaultTableModel actualizarTabla(){
//        String[] columnas = {"ID", "Nombre", "Edad", "Nota 1", "Nota 2", "Nota 3", "Definitiva"};
//        DefaultTableModel tabla = new DefaultTableModel(columnas, 0);
//        
//        for (int i = 0; i < estudiantes.size(); i++){
//            Estudiante estudiante = estudiantes.get(i);
//            double[] notas = estudiante.getNotas();
//            Object[] fila = {
//                estudiante.getId(),
//                estudiante.getNombre(),
//                estudiante.getEdad(),
//                notas[0],
//                notas[1],
//                notas[2],
//                estudiante.calcularNotaFinal()
//            };
//            tabla.addRow(fila);
//        }
//        return tabla;
//    }
    
    
    public Estudiante crearEstudiante(String nombre, String edad, String id){
        return new Estudiante(nombre, Integer.parseInt(edad), Integer.parseInt(id));
    }
    
    public Estudiante crearEstudiante(String nombre, String edad, String id, String[] notas){
        double[] notasNum = new double[3];
        
        for (int i = 0; i < notasNum.length; i++){
            notasNum[i] = Double.parseDouble(notas[i]);
        }
        return new Estudiante(nombre, Integer.parseInt(edad), Integer.parseInt(id), notasNum);
    }
    
    public ArrayList<Estudiante> getEstudiantes(){
        return this.estudiantes;
    }
}
