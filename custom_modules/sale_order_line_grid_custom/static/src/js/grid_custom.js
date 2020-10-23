odoo.define('sale_order_line_grid_custom.grid_custom_js', function (require) {
    "use strict";

    var FieldChar = require('web.basic_fields').FieldChar;
    var FieldOne2Many = require('web.relational_fields').FieldOne2Many;
    var ListFieldText = require('web.basic_fields').ListFieldText;
    var ListRenderer = require('web.ListRenderer');
    
    var SectionAndNoteListRenderer = require("account.section_and_note_backend");
    var FieldRegistry = require('web.field_registry');

    // var SectionAndNoteListRenderer = ListRenderer.extend({
        
    //     _renderBodyCell: function (record, node, index, options) {
    //         var $cell = this._super.apply(this, arguments);
    
    //         var isSection = record.data.display_type === 'line_section';
    //         var isNote = record.data.display_type === 'line_note';
    //         console.log("NUEVO");
    
    //         if (isSection || isNote) {
    //             if (node.attrs.widget === "handle") {
    //                 return $cell;
    //             } else if (node.attrs.name === "name") {
    //                 var nbrColumns = this._getNumberOfCols();
    //                 if (this.handleField) {
    //                     nbrColumns--;
    //                 }
    //                 if (this.addTrashIcon) {
    //                     nbrColumns--;
    //                 }
    //                 $cell.attr('colspan', nbrColumns);
    //             } else {
    //                 $cell.removeClass('o_invisible_modifier');
    //                 return $cell.addClass('o_hidden');
    //             }
    //         }
    
    //         return $cell;
    //     },
    // });
    // return SectionAndNoteListRenderer;
    
    SectionAndNoteListRenderer.include({
        
        init: function () {
            this._super.apply(this, arguments)
        },
        
        _renderBodyCell: function (record, node, index, options) {
            
            var $cell = this._super.apply(this, arguments);
    
            var isSection = record.data.display_type === 'line_section';
            var isNote = record.data.display_type === 'line_note';
    
            if (isSection || isNote) {
                if (node.attrs.widget === "handle") {
                    return $cell;
                } else if (node.attrs.name === "name" || node.attrs.name === "x_mostrar_seccion") {
                    var nbrColumns = this._getNumberOfCols();
                    if (this.handleField) {
                        nbrColumns--;
                    }
                    if (this.addTrashIcon) {
                        nbrColumns--;
                    }
                    $cell.attr('colspan', nbrColumns);
                } else {
                    $cell.removeClass('o_invisible_modifier');
                    return $cell.addClass('o_hidden');
                }
            }
            return $cell;
        }
    });
    return SectionAndNoteListRenderer;

    // var SectionAndNoteListRendererCustom = SectionAndNoteListRenderer.extend({

    //     _renderBodyCell: function (record, node, index, options) {
    //         var $cell = this._super.apply(this, arguments);

    //         var isSection = record.data.display_type === 'line_section';
    //         var isNote = record.data.display_type === 'line_note';

    //         console.log("NUEVO");
    //         if (isSection || isNote) {
    //             if (node.attrs.widget === "handle") {
    //                 return $cell;
    //             } else if (node.attrs.name === "name" || node.attrs.name === "x_mostrar_seccion") {
    //                 var nbrColumns = this._getNumberOfCols();
    //                 if (this.handleField) {
    //                     nbrColumns--;
    //                 }
    //                 if (this.addTrashIcon) {
    //                     nbrColumns--;
    //                 }
    //                 $cell.attr('colspan', nbrColumns);
    //             } else {
    //                 $cell.removeClass('o_invisible_modifier');
    //                 return $cell.addClass('o_hidden');
    //             }
    //         }
    //         return $cell;
    //     }
    // });

    // //FieldRegistry.add('section_and_note_text', SectionAndNoteListRendererCustom);
    // return SectionAndNoteListRendererCustom;
});