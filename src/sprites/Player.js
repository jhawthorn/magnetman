import Phaser from 'phaser'

export default class extends Phaser.Sprite {
  constructor ({ game, x, y, map }) {
    super(game, x, y, 'player');

    game.physics.enable(this, Phaser.Physics.ARCADE);

    this.map = map;

    this.body.collideWorldBounds = true;
    this.body.gravity.y = 500;
    this.body.maxVelocity.y = 300;
    this.body.maxVelocity.x = 150;
    this.body.linearDamping = 1;
    this.body.setSize(20, 26, 0, 0);

    const fps = 15;
    this.animations.add('walk', [0,1,2,3,4,5,6,7], fps, true);
    this.animations.add('stand', [8]);
    this.animations.add('grip', [10]);
    this.animations.add('jump', [11]);

    this.animations.play('walk');

    this.anchor.setTo(0.5, 1);

    this.cursors = game.input.keyboard.createCursorKeys();
    this.jumpButton = game.input.keyboard.addKey(Phaser.Keyboard.Z);
  }

  isGripping() {
    if (this.body.blocked.left) {
      const tile = this.map.getTileWorldXY(this.body.x - 1, this.body.y + this.body.halfHeight);
      return tile && tile.index === 15;
    } else if (this.body.blocked.right) {
      const tile = this.map.getTileWorldXY(this.body.x + this.body.width + 1, this.body.y + this.body.halfHeight);
      return tile && tile.index === 15;
    } else {
      return false;
    }
  }

  update () {
    if(this.body.deltaX() < -1) {
      this.scale.x = 1;
    } else if(this.body.deltaX() > 1) {
      this.scale.x = -1;
    }

    if (this.cursors.left.isDown) {
      this.body.velocity.x -= this.body.onFloor() ? 25 : 15;
      this.animations.play('walk');
    }

    if (this.cursors.right.isDown) {
      this.body.velocity.x += this.body.onFloor() ? 25 : 15;
      this.animations.play('walk');
    }

    if (!this.cursors.right.isDown && !this.cursors.left.isDown) {
      this.animations.play('stand');
    }


    this.body.allowGravity = true;

    if (this.body.onFloor()) {
      /* on ground */
      this.body.drag.x = 800;
      if (this.jumpButton.justPressed()) {
        this.body.velocity.y = -500;
      }
    } else if (this.isGripping()) {
      /* gripping? */
      this.body.velocity.y = 0;
      this.body.allowGravity = false;
      this.animations.play('grip');

      if (this.jumpButton.justPressed()) {
        this.body.velocity.y = -250;
        if (this.body.blocked.left) {
          this.body.velocity.x = 140;
        } else {
          this.body.velocity.x = -140;
        }
      }
    } else {
      /* in air */
      this.body.drag.x = 100;
      this.body.drag.y = 200;
      this.animations.play('jump');
    }
  }
}
