(function(){
  // Kanban drag+drop: when card moved between lists, POST form to /ui/cards/{id}/move
  function init(){
    document.querySelectorAll(".cardlist").forEach(function(el){
      new Sortable(el, {
        group: "kanban",
        animation: 150,
        onAdd: function (evt) {
          const cardId = evt.item.getAttribute("data-card-id");
          const listId = evt.to.getAttribute("data-list-id");
          const formData = new FormData();
          formData.append("list_id", listId);
          fetch(`/ui/cards/${cardId}/move`, { method: "POST", body: formData });
        }
      });
    });
  }
  document.addEventListener("DOMContentLoaded", init);
})();
