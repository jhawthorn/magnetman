import Phaser from 'phaser'

export default class extends Phaser.Sprite {
  constructor ({ game, x, y, map }) {
    super(game, x, y, 'door');

    game.physics.enable(this, Phaser.Physics.ARCADE);
    this.body.allowGravity = false;
    this.body.immovable = true;

    /* 2px midpoint of actual door */
    this.body.setSize(2, 8, 23, 40);
  }
}
