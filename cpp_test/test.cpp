#include <cstddef>

typedef struct _spl_dllist_object spl_dllist_object;

typedef struct _spl_ptr_llist_element {
	struct _spl_ptr_llist_element *prev;
	struct _spl_ptr_llist_element *next;
	// int                            rc;
	// zval                           data;
} spl_ptr_llist_element;


typedef struct _spl_ptr_llist {
	spl_ptr_llist_element   *head;
	spl_ptr_llist_element   *tail;
	// spl_ptr_llist_dtor_func  dtor;
	// spl_ptr_llist_ctor_func  ctor;
	int count;
} spl_ptr_llist;

struct _spl_dllist_object {
	spl_ptr_llist         *llist;
	int                    traverse_position;
	spl_ptr_llist_element *traverse_pointer;
	// int                    flags;
	// zend_function         *fptr_offset_get;
	// zend_function         *fptr_offset_set;
	// zend_function         *fptr_offset_has;
	// zend_function         *fptr_offset_del;
	// zend_function         *fptr_count;
	// zend_class_entry      *ce_get_iterator;
	// zval                  *gc_data;
	// int                    gc_data_count;
	// zend_object            std;
};


int main(){
    spl_ptr_llist_element first, second, third;
    first.prev = NULL, first.next = &second;
    second.prev = &first, second.next = &third;
    third.prev = &second, third.next = NULL;

    spl_ptr_llist ptr_list{&first, &third};

    spl_dllist_object dlllist{&ptr_list, 0, &first};

    return 0;
}