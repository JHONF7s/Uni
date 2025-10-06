
package modelo;

public class Estudiante {
    private String nombre;
    private int edad;
    private int id;
    private double[] notas;
    
    
    
    public Estudiante(String nombre, int edad, int id){
        this.nombre = nombre;
        this.edad = edad;
        this.id = id;
        this.notas = new double[3];
    }
    
    public Estudiante(String nombre, int edad, int id, double[] notas){
        this.nombre = nombre;
        this.edad = edad;
        this.id = id;
        this.notas = notas;
    }
    
    
    
    public double calcularNotaFinal(){
        double suma = 0;
        for (int i = 0; i < notas.length; i++){
            suma += notas[i];
        }
        return suma / notas.length;
    }
    
    
    
    public String getNombre(){return this.nombre;}
    public int getEdad(){return this.edad;}
    public int getId(){return this.id;}
    public double[] getNotas(){return this.notas;}
    
    
    
    public void setNombre(String nombre){
        this.nombre = nombre;
    }
    public void setEdad(int edad){
        this.edad = edad;
    }
    public void setNotaIndex(int indice, double nota){
        this.notas[indice] = nota;
    }
    public void setNotas(double[] notas){
        this.notas = notas;
    }
}
