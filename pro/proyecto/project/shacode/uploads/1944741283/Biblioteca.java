package Biblioteca;

import java.util.ArrayList;
import java.util.List;

public class Biblioteca {
    private List<Libro> libros;
    private List<Usuario> usuarios;

    public Biblioteca(){
        this.libros = new ArrayList<>();
        this.usuarios = new ArrayList<>();
    }

    public boolean registrarLibro(Libro libro){
        // TODO: Agregar libro si ISBN no se repite
        if (buscarLibroPorIsbn(libro.getIsbn()) == null){
            libros.add(libro);
            return true;
        }
        return false;
    }
    public boolean removerLibro(String isbn){
        // TODO: Eliminar libro si existe y no esta prestado
        Libro libro = buscarLibroPorIsbn(isbn);
        if (libro != null && !libro.isPrestado()){
            libros.remove(libro);
            return true;
        }
        return false;
    }
    public Libro buscarLibroPorIsbn(String isbn){
        // TODO: Buscar libro y retornar
        for (int i = 0; i < libros.size(); i++){
            Libro libro = libros.get(i);
            if (libro.getIsbn().equals(isbn)) return libro;
        }
        return null;
    }
    public List<Libro> buscarLibrosDisponibles(){
        // TODO: Retornar todos los libros no prestados
        List<Libro> disponibles = new ArrayList<>();
        for (int i = 0; i < libros.size(); i++){
            Libro libro = libros.get(i);
            if (libro.isPrestado())
                disponibles.add(libro);
        }
        return disponibles;
    }
    public void registrarUsuario(Usuario usuario){
        usuarios.add(usuario);
    }
}
// hola pool chupeme el pene 
//Trabajo en equipo
// aqui escribio jhon 

HOLA
CHUPELCHEI

// andres haga los metodos de chupar pene
System.out.println("chuparpene");
chupeme el pene, delete.System34 de Farfo
esta bien
